from django.shortcuts import render
from subprocess import Popen, PIPE
import subprocess

def index(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        output = run_recon(domain)
        
        asns = []
        emails = []
        urls = []
        hosts = []
        ips = []
        
        if output:
            lines = output.split('\n')
            section = None
            
            for line in lines:
                if line.startswith('[*] ASNS found:') or line.startswith('[*] No ASNS found.'):
                    section = 'asns'
                elif line.startswith('[*] Interesting Urls found:') or line.startswith('[*] No Urls found.'):
                    section = 'urls'
                elif line.startswith('[*] IPs found:') or line.startswith('[*] No IPs found.'):
                    section = 'ips'
                elif line.startswith('[*] Emails found:') or line.startswith('[*] No emails found.'):
                    section = 'emails'
                elif line.startswith('[*] Hosts found:')or line.startswith('[*] No hosts found.'):
                    section = 'hosts'               
                elif section:
                    if line.strip() != '':
                        if section == 'asns':
                            asns.append(line.strip())
                        elif section == 'urls':
                            urls.append(line.strip())
                        elif section == 'ips':
                            ips.append(line.strip())
                        elif section == 'emails':
                            emails.append(line.strip())
                        elif section == 'hosts':
                            hosts.append(line.strip())
        
        return render(request, 'index.html', {'asns': asns, 'emails': emails, 'urls': urls, 'hosts': hosts, 'ips': ips, 'domain': domain})
    
    return render(request, 'index.html')

# from django.shortcuts import render

# def index(request):
#     if request.method == 'POST':
#         domain = request.POST.get('domain')
#         output = run_recon(domain)
#         return render(request, 'index.html', {'output': output})
#     return render(request, 'index.html')

def run_recon(domain):
    cmd = f'python ./theHarvester/theHarvester.py -d {domain} -b all"'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    print(output)
    return output.decode('utf-8')

def home_view(request):
    return render(request, 'home.html')