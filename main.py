import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ------------------------------------------------
# 🌐 가짜 웹 서버 설정 (Render 무료 호스팅을 위한 필수 코드)
# ------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    # Render가 할당하는 PORT 환경 변수를 사용하거나, 없으면 8080을 사용
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------------------

# 봇의 인텐트 설정 (메시지 내용을 읽기 위해 필요합니다)
intents = discord.Intents.default()
intents.message_content = True

# 명령어 접두사 설정 (예: !오픈, !종료)
bot = commands.Bot(command_prefix='!', intents=intents)

# ==========================================
# ⚙️ 설정 부분 (여기서 원하는 내용을 수정하세요)
# ==========================================

# 상태 메시지 (소개글)
BOT_ACTIVITY_TEXT = "현풍버스 시뮬레이터 RP 서버 관리 중"

# 서버 일정 및 24시간 가동 안내 메시지
SERVER_SCHEDULE_TEXT = """
**[ 🕒 서버 가동 및 오픈 일정 안내 ]**
✅ **서버 가동**: 24시간 상시 가동 중! (서버 자체는 24시간 켜져 있습니다)
📅 **RP 오픈 일정**: 
- 평일: 오후 6시 ~ 오후 7시30분 (시간을 수정해주세요)
- 주말/공휴일: 오후 15시 ~ 오후 16시 30분 (시간을 수정해주세요)
🔗 **접속 안내**: [접속 방법이나 링크를 여기에 적어주세요]
"""

@bot.event
async def on_ready():
    """봇이 실행될 때 한 번 호출됩니다."""
    print(f'✅ 봇이 로그인되었습니다: {bot.user.name} (ID: {bot.user.id})')
    # 봇의 상태 메시지(소개글)를 설정합니다.
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=BOT_ACTIVITY_TEXT))

@bot.command(name='오픈')
@commands.has_permissions(administrator=True) # 관리자 권한이 있는 사람만 사용 가능
async def open_server(ctx):
    """서버 오픈을 알립니다."""
    embed = discord.Embed(
        title="🟢 현풍버스 시뮬레이터 RP 서버 오픈!", 
        description="지금 바로 서버에 접속하여 RP를 즐겨주세요!", 
        color=discord.Color.green()
    )
    # 24시간 가동 및 일정 정보 추가
    embed.add_field(name="안내", value=SERVER_SCHEDULE_TEXT, inline=False)
    embed.set_footer(text="AIㆍ서버 관리 봇")
    
    await ctx.send(embed=embed)
    # 만약 에브리원 멘션을 원하시면 아래 줄의 주석(#)을 지워주세요.
    # await ctx.send("@everyone")

@bot.command(name='종료', aliases=['닫힘'])
@commands.has_permissions(administrator=True)
async def close_server(ctx):
    """서버 종료(닫힘)를 알립니다."""
    embed = discord.Embed(
        title="🔴 RP 서버가 종료(닫힘) 되었습니다.", 
        description="오늘 진행된 RP에 참여해주신 모든 분들께 감사드립니다.\n다음 오픈 시간에 뵙겠습니다!", 
        color=discord.Color.red()
    )
    embed.set_footer(text="AIㆍ서버 관리 봇")
    await ctx.send(embed=embed)

@bot.command(name='정보', aliases=['일정'])
async def server_info(ctx):
    """언제든지 서버 일정과 정보를 확인할 수 있는 명령어입니다."""
    embed = discord.Embed(title="ℹ️ 서버 일정 및 정보", color=discord.Color.blue())
    embed.add_field(name="상세 내용", value=SERVER_SCHEDULE_TEXT, inline=False)
    embed.set_footer(text="AIㆍ서버 관리 봇")
    await ctx.send(embed=embed)


# ==========================================
# 🔑 봇 실행 부분
# ==========================================
if __name__ == '__main__':
    # 1. 24시간 가동을 위한 가짜 웹 서버 실행
    keep_alive()
    
    # 2. os.environ을 사용해 안전하게 토큰을 가져옴 (코드에 토큰이 노출되지 않음!)
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
    if BOT_TOKEN is None:
        print("❌ 오류: 'DISCORD_BOT_TOKEN' 환경 변수가 설정되지 않았습니다.")
        print("Render의 Environment 항목이나 로컬 컴퓨터 환경 변수에 토큰을 추가해주세요.")
    else:
        try:
            print("⏳ 봇을 시작합니다...")
            bot.run(BOT_TOKEN)
        except Exception as e:
            print(f"❌ 봇 실행 중 오류가 발생했습니다.\n오류 내용: {e}")
