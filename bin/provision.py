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

debug = False
verbose = False

def yaml_load(filename):
  f = open(filename)
  tmp = yaml.load(f)
  f.close()
  return tmp

def create_machine(opts):
  '''This calls gcutil to add an instance :)'''
  print '- Creating a machine. Options: ', opts
  project_base = opts['project-base']
  command = '''gcutil \
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
  print 'command: ', command
  os.system(command)
  
def test_machine(conf):
  '''Have to retrieve machine info from gcutil.. like gcutil listinstance.
  Hostname is already available in opts'''
  print 'TODO: Running tests substituting __HOSTNAME__ with: ', conf['hostname']
  pass

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
  
def gce_provision(project):
  global debug
  print '= Provisioning:' , project, '='
  # loading conf from yaml
  dfltConf = yaml_load('projects/_common/project.yml')
  projConf = yaml_load('projects/%s/project.yml' % project)
  #conf.update(dfltConf) # takes dflt conf and overwrites things in common
  # super cool but shallow merge!
  #conf = dict(dfltConf, **projConf) # takes dflt conf and overwrites things in common
  conf = yaml_merge(copy.deepcopy(projConf),dfltConf)
  print 'Project: ', conf['project']['name']
  if debug:
    print 'dflt: ', dfltConf['gce']
    print 'proj: ', projConf['gce']
    print 'merge:', conf['gce']
  print ' - all:  ', conf
  #print ' - Proj: ', conf['project']
  #print 'Project: ', conf['project']['name']
  create_machine(conf['gce'])
  test_machine(conf['gce'])


def main():
  global debug
  global verbose
  version = '1.0'
  github_user = 'palladius'
  project = ''
  print 'argv (before): ', sys.argv
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
  project = depured_argv[0]
  gce_provision(project)
  
  
main()