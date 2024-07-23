import subprocess
import re

def parse_ansible_output(text):
    os_pattern = re.compile(r"The operating system is (.*?)\s+\((.*?)\)\s+with kernel version (.*)\n")
    match = os_pattern.search(text)
    
    if match:
        os_name = match.group(1)
        os_version = match.group(2)
        kernel_version = match.group(3)
        return os_name, os_version, kernel_version
    else:
        return None, None, None

def run_ansible_playbook():
    try:
        # Run the ansible-playbook command
        result = subprocess.run(
            ['ansible-playbook', '-i', 'ansible/hosts.ini', 'ansible/gather_facts.yml'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Capture the output
        output = result.stdout
        
        # Parse the output
        os_name, os_version, kernel_version = parse_ansible_output(output)
        
        # Output the results
        print(f"Operating System: {os_name}")
        print(f"OS Version: {os_version}")
        print(f"Kernel Version: {kernel_version}")
        return (os_name, os_version, kernel_version)
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Run the ansible playbook and parse the output
run_ansible_playbook()
