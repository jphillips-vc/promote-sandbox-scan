# imediately after the sandbox scan finishes without breaking build, execute this as a post step to promote the latest sandbox scan
#
import os
import subprocess
import sys
import json
import xml.etree.ElementTree as ET
#
JavaWrapperVersion="21.6.8.0" # capture latest version https://search.maven.org/search?q=a:vosp-api-wrappers-java 
#
def promote_sandbox():
      
      try:
            # GET APP LIST
            # applist_xml = os.system("java -jar VeracodeJavaAPI.jar -action getapplist")
            # print(applist_xml)
            
            # DOWNLOAD API WRAPPER            
            os.system('curl -sSo VeracodeJavaAPI.jar https://repo1.maven.org/maven2/com/veracode/vosp/api/wrappers/vosp-api-wrappers-java/'+str(JavaWrapperVersion)+'/vosp-api-wrappers-java-'+str(JavaWrapperVersion)+'.jar')
            
            #obtain the app id from the command line argument
            appid = str(sys.argv[1])
            
            #run the java call as a subprocess and store results in buildinfo_xml
            buildinfo_xml = subprocess.run(["java", "-jar", "VeracodeJavaAPI.jar", "-action", "getbuildinfo" , "-appid", appid], stdout=subprocess.PIPE, text=True)
            
            # write xml response to buildinfo as a dict
            buildinfo = ET.fromstring(buildinfo_xml.stdout)
            
            for x in buildinfo:
                  # set variables
                  build_id = str(x.attrib['build_id'])
                  results_ready = x.attrib['results_ready']
                  rules_status = x.attrib['rules_status']
                  # if results are ready and policy evaluattion passed proceed with promoting scan
                  if results_ready=='true' and rules_status=='Pass':
                        # execute sandbox promotion
                        promote_sandbox_cmd = subprocess.run(["java", "-jar", "VeracodeJavaAPI.jar", "-action", "promotesandbox" , "-buildid", build_id], stdout=subprocess.PIPE, text=True)
                        print(promote_sandbox_cmd.stdout)

                  else:
                        # break
                        print("Alert, build didn't promote")
      except:
            sys.exit(0)


def main():
      #
      promote_sandbox()
      #

main()