def pull_run(parallel_jobs, cmds):
    '''
    run pull of jobs
    input:
        parallel_jobs: integer, how many jobs at once
        cmds: list of commands
    '''
    with ThreadPoolExecutor(max_workers=parallel_jobs) as executor:
        futures = executor.map(exec_parallel, cmds)
        #executor.shutdown(wait=True)