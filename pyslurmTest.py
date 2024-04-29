import pyslurm

def get_job_details(job_id):
    try:
        job_info = pyslurm.job().find_id(job_id)
        if job_info:
            print(f"Job Details for ID {job_id}:")
            # Check if the result is a list and iterate over it
            if isinstance(job_info, list):
                for job in job_info:
                    print("----")
                    for key, value in job.items():
                        print(f"{key}: {value}")
            else:
                # If it's not a list, process as a single dictionary
                for key, value in job_info.items():
                    print(f"{key}: {value}")
        else:
            print(f"No job found with ID {job_id}")
    except Exception as e:
        print(f"Error retrieving job details: {str(e)}")

# Create a job dictionary that describes the job
job_dict = {
    'account': 'agr240009',
    'nodes': 1,
    'ntasks': 1,
    'time': '00:05:00',
    'job_name': 'test_job',
    'output': 'output.log',
    'error': 'error.log',
    'partition': 'shared',
    'mail-user': 'dgamdha@iastate.edu',
    'mail-type': 'ALL',
    'script': 'temp.sh'
}

# Submit the job
try:
    job_id = pyslurm.job().submit_batch_job(job_dict)
    print(f"Job submitted successfully with ID: {job_id}")
except Exception as e:
    print(f"Failed to submit job: {str(e)}")

# Get job details
get_job_details(job_id)



'''
Job Details for ID 4917380:
----
account: agr240009
accrue_time: Unknown
admin_comment: None
alloc_node: login04
alloc_sid: 2092372
array_job_id: None
array_task_id: None
array_task_str: None
het_job_id: None
het_job_id_set: None
het_job_offset: None
array_max_tasks: None
assoc_id: 11890
batch_flag: 1
batch_features: None
batch_host: None
billable_tres: 4294967294.0
bitflags: 402669568
boards_per_node: 0
burst_buffer: None
burst_buffer_state: None
command: None
comment: None
contiguous: False
core_spec: 65534
cores_per_socket: 65534
cpus_per_task: 1
cpus_per_tres: None
cpu_freq_gov: 4294967294
cpu_freq_max: 4294967294
cpu_freq_min: 4294967294
dependency: None
derived_ec: 0:0
eligible_time: 1714173955
end_time: 0
exc_nodes: []
exit_code: 0:0
features: []
group_id: 7001427
job_id: 4917380
job_state: PENDING              // 
last_sched_eval: 2024-04-26T19:25:55
licenses: {}
max_cpus: 0
max_nodes: 0
mem_per_tres: None
name: test_job
network: None
nodes: None
nice: 0
ntasks_per_core: 65535
ntasks_per_core_str: 65535
ntasks_per_node: 0
ntasks_per_socket: 65535
ntasks_per_socket_str: 65535
ntasks_per_board: 0
num_cpus: 1
num_nodes: 1
num_tasks: 1
partition: shared
mem_per_cpu: True
min_memory_cpu: 1896
mem_per_node: False
min_memory_node: None
pn_min_memory: 1896
pn_min_cpus: 1
pn_min_tmp_disk: 0
power_flags: 0
priority: 34259
profile: 0
qos: cpu
reboot: 0
req_nodes: []
req_switch: 0
requeue: True
resize_time: 0
restart_cnt: 0
resv_name: None
run_time: 0
run_time_str: 00:00:00
sched_nodes: None
selinux_context: None
shared: OK
show_flags: 19
sockets_per_board: 0
sockets_per_node: 65534
start_time: 0
state_reason: Priority
std_err: /anvil/scratch/x-dgamdha/projects/leap_hi/software/runs/adm_runs/error.log
std_in: /dev/null
std_out: /anvil/scratch/x-dgamdha/projects/leap_hi/software/runs/adm_runs/output.log
submit_time: 1714173955
suspend_time: 0
system_comment: None
time_limit: 30
time_limit_str: 0-00:30:00
time_min: 0
threads_per_core: 65534
tres_alloc_str: None
tres_bind: None
tres_freq: None
tres_per_job: None
tres_per_node: None
tres_per_socket: None
tres_per_task: None
tres_req_str: cpu=1,mem=1896M,node=1,billing=1
user_id: 7940354
wait4switch: 0
wckey: None
work_dir: /anvil/scratch/x-dgamdha/projects/leap_hi/software/runs/adm_runs
cpus_allocated: {}
cpus_alloc_layout: {}

'''