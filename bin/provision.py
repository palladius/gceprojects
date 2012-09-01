#!/usr/bin/python

'''Usage: provision [-hdv] <project name>'''

import sys
import getopt
import yaml

#def load_conffile(project):
#  f = open('project.yml')
#  dataMap = yaml.load(f)
#  f.close()
  
def create_machine(opts):
  print 'Creating a machine. Options: ', opts
  
  
def gce_provision(project):
  print 'Trying to provision project:' , project
  f = open('projects/%s/project.yml' % project)
  dataMap = yaml.load(f)
  f.close()
  print 'buridone: ', dataMap
  print ' - GCE:  ', dataMap['gce']
  print ' - Proj: ', dataMap['project']
  create_machine(dataMap['gce'])



def main():
  version = '1.0'
  verbose = False
  debug = False
  github_user = 'palladius'
  project = ''

  #print getopt.getopt(['-a', '-bval', '-c', 'val'], 'ab:c:')
  print 'argv (before): ', sys.argv
  options, depured_argv = getopt.getopt(sys.argv[1:], 'g:vd', ['githubuser=', 
                                                         'verbose',
                                                         'debug',
                                                         ])
  #print 'OPTIONS   :', options
  
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