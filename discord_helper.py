import discord
import chestnut_towers
from decouple import config

WEBHOOK_URL = config('DISCORD_WEBHOOK')

def send_alert(available_floor_plans):
  webhook = discord.Webhook.from_url(WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
  mentions = discord.AllowedMentions()
  for embed_list in create_embeds(available_floor_plans):
    webhook.send('@everyone Found availabilities', wait=True, allowed_mentions=mentions, embeds=embed_list)

def create_embeds(available_floor_plans):
  for chunk in __chunk(available_floor_plans, 10): # 10 embeds max per message
    embeds = []
    for floor_plan in chunk:
      dict = {
        'color': discord.Colour.green().value,
        'thumbnail': {
          'url': floor_plan.layout
        },
        'footer': {
          'text': chestnut_towers.url()
        },
        'fields': [
          {
            'name': 'Layout',
            'value': floor_plan.floor_plan,
            'inline': True
          },
          {
            'name': 'Sq Ft',
            'value': floor_plan.sq_ft,
            'inline': True
          },
          {
            'name': 'Rent',
            'value': floor_plan.rent,
            'inline': True
          },
          {
            'name': 'Available',
            'value': floor_plan.availability,
            'inline': True
          }
        ]
      }
      embeds.append(discord.Embed.from_dict(dict))
    yield  embeds

def __chunk(lst, n):
  return [lst[i:i + n] for i in range(0, len(lst), n)]