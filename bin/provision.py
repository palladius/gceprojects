#!/usr/bin/python

'''Usage: provision [-hdv] <project name>





GCutil test:

gcutil addinstance hostname 
  --project_id=google.com:jeffsilverman 
  --description='[jeffsilverman.py] Jeff bug see b://7087193 :"gsutil was installed incorrectly"'   
  --tags='ric,py,v103,ric,py,v103,ric,py,v103,ric,py,v103,ric,py,v103'   
  --zone='us-east1-a'   
  --machine_type='n1-standard-1'   
  --metadata_from_file=startup-script:./projects/riclib/scripts/common-startup-script.sh   
  --metadata=startup-metadata:project:jeffsilverman:e=py^2   
  --metadata=author:$USER   
'''

import sys
import getopt
import yaml
import copy
import os
import subprocess
import tempfile



debug = False
verbose = False
#machine_ip = '_no_ip_'
#machine_host = '_no_hostname_'
machine =  {'foo': 'bar42', 'description': 'this is the machien hash info'}
gce_project = '_not_defined_yet_'

def yellow(s):
  return "\033[1;33m%s\033[0m" % s

def yaml_load(filename):
 try:
  f = open(filename)
  tmp = yaml.load(f)
  f.close()
  return tmp
 except:
  print 'FATAL Cant yaml open:', filename
  exit(2)

def usage():
  print "%s -dhv <PROJECT_NAME>" % sys.argv[0]
  #print " Tip: find project names under projects/"
  #project_list = os.system()
  #project_list = subprocess.Popen('ls projects/ | egrep -v ^_', shell=True,stdout=subprocess.PIPE).communicate()[0]
  project_list = esegui('ls projects/ | egrep -v ^_common')
  print " Available projects: ", ' '.join(project_list.split('\n')) 
  exit(1)
  
def esegui(script):
  return subprocess.Popen(script, shell=True,stdout=subprocess.PIPE).communicate()[0]
  
def subtitute_template_stuff(str):
  global machine
  str = str.replace('''{{project}}''',gce_project)
  for key in machine:
    str = str.replace('''{{%s}}''' % key, machine[key]) 
  return str

def merged_metadata_script():
  global gce_project
  f = tempfile.NamedTemporaryFile(delete=False)
  for filename in [ 'projects/_common/first-boot.sh', 'projects/%s/first-boot.sh' % gce_project ]:
    tempf = open(filename, "r")
    #print 'File: ',tempf
    f.write(tempf.read())
  return f.name

def create_machine( opts):
  '''This calls gcutil to add an instance :)'''
  global machine
  print '- Creating a machine. Options: ', opts
  
  # TODO assemble command in proper way, building from hash
  create_options = {
    '--project_id':          opts['project-base'] + ':' + opts['project'],
    '--tags':                ','.join(opts['tags']),
    '--zone':                opts['zone'],
    '--machine_type':        opts['machine-type'],
    '--metadata_from_file':  'startup-script:%s' % merged_metadata_script(),
  }
  command = 'gcutil addinstance %s' % opts['hostname'] 
  for k in create_options:
    command = '%s %s=%s' % (command, k, create_options[k])
  # DELETEME if it works!
  command_old = '''gcutil \
    --project_id="%s:%s" \
    addinstance %s \
    --tags="%s"\
    --zone=%s \
    --machine_type=%s \
    --metadata_from_file=startup-script:%s \
    ''' % (opts['project-base'],opts['project'],opts['hostname'],
           ','.join(opts['tags']),
           opts['zone'],
           opts['machine-type'],
           opts['metadata']['startup-script'],
        )
  # TODO do a for cycle for all metadata :)
  command = subtitute_template_stuff(command)
  print '*** Subtituted command: ', command
  #print 'NEW Options: ', create_options
  os.system(command)
  machine['ip'] = esegui("""gcutil --project=%s:%s getinstance %s |grep 'external ip' | awk '{print $5}'""" % (opts['project-base'],opts['project'],opts['hostname']) ).split()[0]
  machine['hostname'] = opts['hostname']
  
def test_machine( conf):
  '''Have to retrieve machine info from gcutil.. like gcutil listinstance.
  Hostname is already available in opts'''
  #print 'TODO: Running tests substituting {{hostname}} with: ', conf['hostname']
  testdir =  'projects/%s/test/' % gce_project
  for filename in os.listdir(testdir):
   #if filename.match('*.sh'):
    print yellow(' = Testing: '+filename+' =')
    tmp = tempfile.NamedTemporaryFile(delete=False) # for debug, it should safely be TRUE (no needed after end
    #print 'tmp:',tmp
    orig = open(testdir+filename,'r')
    tmp.write(subtitute_template_stuff(orig.read()))
    tmp.close() # flush the read
    if debug:
      print 'Substituted file is : ', tmp.name
      print 'Original content: ', esegui('cat '+testdir+filename)
      print 'Substituted content: executing: ', ('cat '+tmp.name)
      print 'Substituted content: ', esegui('cat '+tmp.name)
    ret = os.system('sh %s' % tmp.name) # assert it ends with .sh
    print 'return: ', ret
    if ret != 0:
      print 'ERROR on test: ', filename, '; exit=',ret
    #tmp.unlink()

# deep merge of configuration trees! Yay!
def yaml_merge(user, default):
    if isinstance(user,list) and isinstance(default,list): # array
      #return user + default # works but can have duplicates
      return  list(set(user + default)) # uniq'd
    if isinstance(user,dict) and isinstance(default,dict): # hash
        for k,v in default.iteritems():
            if k not in user:
                user[k] = v
            else:
                user[k] = yaml_merge(user[k],v)
    return user
  
def gce_provision():
  global debug, gce_project
  print yellow('= Provisioning: ' + gce_project+ ' =')
  # loading conf from yaml
  dfltConf = yaml_load('projects/_common/project.yml')
  projConf = yaml_load('projects/%s/project.yml' % gce_project)
  conf = yaml_merge(copy.deepcopy(projConf),dfltConf)
  print 'Project: ', conf['project']['name']
  if debug:
    print 'dflt: ', dfltConf['gce']
    print 'proj: ', projConf['gce']
    print 'merge:', conf['gce']
    print ' - all:  ', conf
  create_machine( conf['gce'])
  print 'Machine important stuff: ', machine
  test_machine(conf['gce'])


def main():
  global debug
  global verbose
  global gce_project
  version = '1.0'
  github_user = 'palladius'
  project = ''
  options, depured_argv = getopt.getopt(sys.argv[1:], 'g:vd', ['githubuser=', 'verbose','debug', ])
  for opt, arg in options:
      if opt in ('-g', '--github-user'):
          github_user = arg
      elif opt in ('-v', '--verbose'):
          verbose = True
      elif opt in ('-d', '--debug'):
          debug = True
      elif opt == '--version':
          version = arg
  
  if (debug):
   print 'github_user  :', github_user
   print 'DEBUG        :', verbose
   print 'VERBOSE      :', verbose
   print 'depured_argv :', depured_argv
   print 'depur_argv l :', len(depured_argv)
  if( len(depured_argv) != 1):
   usage()
   exit(1)
  gce_project = depured_argv[0]
  gce_provision()
  
  
main()