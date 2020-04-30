from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/447960295022002190/M4ggwJ7-FeHyYmm_uZZw4AmAiOVyIjrDRPdtYGTfyIogQSq03JN77EK9igDj2kk75d15", content="!ayy it's 4:20")
response = webhook.execute()
