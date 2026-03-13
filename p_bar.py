import math
import time

async def progress_bar(current, total, message, start):

    now = time.time()
    diff = now - start

    if diff == 0:
        diff = 1

    percentage = current * 100 / total
    speed = current / diff
    elapsed_time = round(diff)

    if speed > 0:
        eta = round((total - current) / speed)
    else:
        eta = 0

    filled = math.floor(percentage / 5)
    bar = "█" * filled + "░" * (20 - filled)

    def humanbytes(size):
        if not size:
            return ""
        power = 2**10
        n = 0
        power_labels = {0: '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power:
            size /= power
            n += 1
        return f"{round(size,2)} {power_labels[n]}"

    text = (
        f"📥 **Downloading...**\n\n"
        f"│{bar}│ {percentage:.2f}%\n\n"
        f"🔹 **Downloaded:** {humanbytes(current)}\n"
        f"🔹 **Total:** {humanbytes(total)}\n"
        f"⚡ **Speed:** {humanbytes(speed)}/s\n"
        f"⏱ **ETA:** {eta}s"
    )

    try:
        await message.edit(text)
    except:
        pass