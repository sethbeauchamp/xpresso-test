# To run the job:
# pyats run job BGP_check_job.py --testbed-file <testbed_file.yaml>
# Description: This job file checks that all BGP neighbors are in Established state
import os

# All run() must be inside a main function
def main(runtime):
    # Find the location of the script in relation to the job file
    bgp_tests = os.path.join(os.path.dirname(__file__), 
                             'check_bgp_vrfs.py')
    import argparse
    import sys
    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--vrf_list', dest = 'vrf_list')
    args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])
    if args.vrf_list:
        vrf_list = args.vrf_list.split()
    else:
        vrf_list = None
    runtime.tasks.run(testscript=bgp_tests, vrf_list = vrf_list)    
    # Execute the testscript
    runtime.tasks.run(testscript=bgp_tests)