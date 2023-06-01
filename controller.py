from discord.ext import commands

class Controller(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Hidden means it won't show up on the default help.
    @commands.command(name="load")
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):

        try:
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name="unload")
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):

        try:
            self.client.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):

        try:
            self.client.unload_extension(cog)
            self.client.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(client):
    client.add_cog(Controller(client))