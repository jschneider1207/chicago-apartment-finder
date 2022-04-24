from chestnut_towers import get_availabilities
from discord_helper import send_alert
import argparse
import sys

def alert(args):
  floor_plan_names = [f for sublist in args.floor_plans for f in sublist]
  availabilities = get_availabilities()
  floor_plans = [f for category in availabilities.categories for f in category.floor_plans if f.floor_plan in floor_plan_names and f.availability > 0]
  
  if len(floor_plans) == 0:
    print('Found no availabilities')
  else:
    print('Found availabilities')
    [print(f) for f in floor_plans]
    send_alert(floor_plans)
  return

def list(args):
  availabilities = get_availabilities()  
  categories = availabilities.categories

  if args.num_bedrooms != None:
    num_bedrooms = [n for sublist in args.num_bedrooms for n in sublist]
    categories = [c for c in categories if c.num_bedrooms in num_bedrooms]
  
  for category in categories:
    print(category)

  return

def main():
  parser = argparse.ArgumentParser(description='Interact with Chestnut Towers apartments.')
  subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', 
                                    help='additional help')

  # parser for 'alert' command
  parser_alert = subparsers.add_parser('alert', help='Send alert if Chectnut Towers floor plan(s) are available.')
  parser_alert.add_argument('floor_plans', metavar='name', type=str, nargs='+', action='append',
                            help='the floor plan name to check availability for.')
  parser_alert.set_defaults(func=alert)

  # parser for 'list' command
  parser_list = subparsers.add_parser('list', help='List floor plans.')
  parser_list.add_argument('-n', '--num-bedrooms', dest='num_bedrooms', metavar='N', type=int, nargs='+', 
                          action='append', choices=range(0,3), help='limit to number of bedrooms')
  parser_list.set_defaults(func=list)

  args = parser.parse_args()
  args.func(args)
  return 0

if __name__ == '__main__':
  sys.exit(main())

  
