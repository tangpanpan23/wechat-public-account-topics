#!/usr/bin/env bash
# 将 hps-test 中「仅同步了表结构、未同步数据」的表，用 mysqldump 把数据同步到 hps-localhost。
# DB 配置写死，与 MCP db-mcp-server 一致：test=测试环境，local=本地。

set -e

# ==================== 配置区域 ====================
# 源库 (hps-test 测试环境 RDS)
SOURCE_HOST="rm-2zef2q80yoia39816.mysql.rds.aliyuncs.com"
SOURCE_PORT="3306"
SOURCE_USER="hps_rw"
SOURCE_PASS="${SOURCE_PASS:-}"   # 通过环境变量传入
SOURCE_DB="hps"

# 目标库 (hps-localhost 本地)
TARGET_HOST="127.0.0.1"
TARGET_PORT="3306"
TARGET_USER="root"
TARGET_PASS="${TARGET_PASS:-}"   # 通过环境变量传入
TARGET_DB="hps"

# 未同步数据的表（仅同步了结构的表）
TABLES=(
  h_dept_role_events
  h_dept_roles
  h_email_send_logs
  h_hc_ehr_request_logs
  h_hc_flow_status
  h_hc_request_events
  h_hcs
  h_message_logs
  h_partners
  h_regions_clone
  h_risk_check_schedules
  h_risk_notice_logs
  h_todo_events
  ps_g_employee
  ps_g_job_1
  ps_g_jobcode_0128
  ps_p_cnrnw
  ps_p_company2
  ps_p_company3
  ps_p_company4
  ps_p_company_0128
  ps_p_jc_stdlvl_0128
  ps_p_location_0128
  ps_p_major
  ps_p_pro
  ps_p_salmonth
  ps_p_school
  ps_p_title
  ps_t_h_p_emplclass_ogg
  ps_t_p_hc_data
  pst_p_person
)

# ==================== 函数 ====================
function usage() {
  echo "用法: $0 [选项]"
  echo ""
  echo "选项:"
  echo "  --dry-run        只打印将要执行的命令，不执行"
  echo "  --table NAME     只同步指定表（可多次指定）"
  echo "  -h, --help       显示帮助"
  echo ""
  echo "环境变量:"
  echo "  SOURCE_PASS      源库密码（测试环境 RDS）"
  echo "  TARGET_PASS      目标库密码（本地）"
  echo ""
  echo "示例:"
  echo "  SOURCE_PASS='xxx' TARGET_PASS='yyy' $0 --dry-run"
  echo "  SOURCE_PASS='xxx' TARGET_PASS='yyy' $0"
  echo "  SOURCE_PASS='xxx' TARGET_PASS='yyy' $0 --table h_message_logs"
  exit 0
}

function check_env() {
  if [[ -z "$SOURCE_PASS" ]] || [[ -z "$TARGET_PASS" ]]; then
    echo "错误: 请设置源库与目标库密码"
    echo ""
    echo "设置方式:"
    echo "  export SOURCE_PASS='源库密码' TARGET_PASS='本地库密码'"
    echo "  $0"
    echo ""
    usage
    exit 1
  fi
}

function sync_tables() {
  local tables=("$@")
  local table_list=$(printf " %s" "${tables[@]}")
  table_list=${table_list:1}  # 去除前导空格
  
  echo "同步 ${#tables[@]} 个表到 localhost..."
  echo "源库: ${SOURCE_HOST}:${SOURCE_PORT}/${SOURCE_DB}"
  echo "目标: ${TARGET_HOST}:${TARGET_PORT}/${TARGET_DB}"
  echo ""
  
  (
    echo "SET SESSION FOREIGN_KEY_CHECKS=0;"
    mysqldump --single-transaction --no-create-info --complete-insert --set-gtid-purged=OFF \
      -h"$SOURCE_HOST" -P"$SOURCE_PORT" -u"$SOURCE_USER" -p"$SOURCE_PASS" "$SOURCE_DB" ${table_list}
    echo "SET SESSION FOREIGN_KEY_CHECKS=1;"
  ) | mysql -h"$TARGET_HOST" -P"$TARGET_PORT" -u"$TARGET_USER" -p"$TARGET_PASS" "$TARGET_DB"
  
  echo "完成: ${#tables[@]} 个表已同步"
}

# ==================== 主流程 ====================
DRY_RUN=
CUSTOM_TABLES=()

# 解析参数
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)   DRY_RUN=1; shift ;;
    --table)     CUSTOM_TABLES+=("$2"); shift 2 ;;
    -h|--help)  usage ;;
    *)           echo "未知选项: $1"; usage ;;
  esac
done

# 使用自定义表或默认表
if [[ ${#CUSTOM_TABLES[@]} -gt 0 ]]; then
  TABLES=("${CUSTOM_TABLES[@]}")
fi

# 检查环境变量
check_env

echo "源库 (test):  ${SOURCE_HOST}:${SOURCE_PORT}/${SOURCE_DB}"
echo "目标库 (local): ${TARGET_HOST}:${TARGET_PORT}/${TARGET_DB}"
echo "表数量: ${#TABLES[@]}"
echo ""

if [[ -n "$DRY_RUN" ]]; then
  echo "--- [DRY-RUN] 将要执行的命令 ---"
  echo "mysqldump --single-transaction --no-create-info --complete-insert --set-gtid-purged=OFF \\"
  echo "  -h${SOURCE_HOST} -P${SOURCE_PORT} -u${SOURCE_USER} -p*** ${SOURCE_DB} \\"
  printf "  %s\n" "${TABLES[@]}"
  echo ""
  echo "mysql -h${TARGET_HOST} -P${TARGET_PORT} -u${TARGET_USER} -p*** ${TARGET_DB}"
  exit 0
fi

sync_tables "${TABLES[@]}"
