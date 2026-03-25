# php

php
// 查询多个员工
$workCodes = ['V0059359', 'V0059369'];

foreach ($workCodes as $workCode) {
$employee = \App\Models\Employee::where('workcode', $workCode)->first();

if (!$employee) {
echo "员工 {$workCode} 不存在，跳过\n";
continue;
}

$certificate = \App\Models\Certificate::where('employee_id', $employee->id)->first();

if (!$certificate) {
echo "员工 {$workCode} 证件信息不存在，跳过\n";
continue;
}

$data = [
'workCode'       => $employee->workcode,
'masterWorkCode' => $employee->master_workcode,
'mobile'         => $employee->mobile,
'mobile_code'    => $employee->mobile_code,
'idNumber'       => $certificate->id_number,
'idType'         => $certificate->id_type,
];

// 同步执行
\App\Jobs\ESignCreateJob::dispatchNow($data);

echo "已为员工 {$workCode} 发起e签宝流程\n";

// 避免请求过快，可以加延迟
usleep(500000); // 延迟0.5秒
}