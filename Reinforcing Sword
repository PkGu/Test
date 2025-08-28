import tkinter as tk
import random
from tkinter import messagebox, simpledialog

# --------- 기본 설정 ----------
weapon_names = [
    "녹슨 검", "철검", "강철검", "강화 철검", "고대검",
    "마검", "화염검", "얼음검", "폭풍검", "천둥검",
    "전설의 검", "신의 검", "신화의 검", "엘프의 검", "드래곤 슬레이어",
    "용의 검", "초월검", "차원의 검", "운명의 검", "우주의 검",
    "시간의 검", "무한의 검", "절대자의 검", "혼돈의 검", "창세의 검",
    "🔥 지존검 🔥", "💥 궁극검 💥", "⚡ 갓검 ⚡", "🌌 멀티버스검 🌌", "💀 울트라 짱짱 센 검 💀"
]
success_rates = [100, 95, 90, 85, 80, 70, 65, 60, 55, 50,
                 50, 45, 40, 35, 30, 30, 25, 20, 15, 10,
                 10, 8, 6, 4, 3, 2, 1.5, 1.2, 1.1, 1]
max_slots = 5  # 초기 슬롯 수

def upgrade_cost(level):
    return 100 + level * 150

def get_weapon_name(level):
    return f"+{level} {weapon_names[level]}"

# --------- 상태 ----------
inventory = []  # 여러 개의 검
selected_index = None
gold = 50000
win_streak = 0

# --------- UI 함수 ----------
def update_ui():
    gold_label.config(text=f"🪙 골드: {gold:,}G")
    weapon_listbox.delete(0, tk.END)
    for i, lvl in enumerate(inventory):
        weapon_listbox.insert(i, get_weapon_name(lvl))

    if selected_index is not None and selected_index < len(inventory):
        level = inventory[selected_index]
        cost_label.config(text=f"💰 강화 비용: {upgrade_cost(level)}G")
        rate_label.config(text=f"📈 성공 확률: {success_rates[level]}%")
        selected_label.config(text=f"선택된 검: {get_weapon_name(level)}")
    else:
        cost_label.config(text="💰 강화 비용: -")
        rate_label.config(text="📈 성공 확률: -")
        selected_label.config(text="선택된 검 없음")
    slot_info_label.config(text=f"🔒 슬롯: {len(inventory)}/{max_slots}")

def game_over():
    messagebox.showerror("💀 게임 오버", "당신은 골드를 모두 잃고 죽었습니다...")
    enhance_button.config(state=tk.DISABLED)
    gamble_button.config(state=tk.DISABLED)
    sell_button.config(state=tk.DISABLED)
    add_button.config(state=tk.DISABLED)
    retry_gamble_button.config(state=tk.DISABLED)

def on_select(event):
    global selected_index
    try:
        selected_index = weapon_listbox.curselection()[0]
    except IndexError:
        selected_index = None
    update_ui()

# --------- 게임 로직 ----------
def add_weapon():
    global gold
    if len(inventory) >= max_slots:
        result_label.config(text=f"⚠️ 인벤토리가 가득 찼습니다. (최대 {max_slots}개)")
        return
    inventory.append(0)
    result_label.config(text="🆕 +0 검이 추가되었습니다.")
    update_ui()

def expand_slot():
    global gold, max_slots
    cost = (max_slots + 1) * 10000
    if gold < cost:
        result_label.config(text=f"❌ 슬롯 확장에 {cost:,}G 필요")
        return
    gold -= cost
    max_slots += 1
    result_label.config(text=f"📦 슬롯이 {max_slots}개로 확장되었습니다! (-{cost:,}G)")
    update_ui()



def enhance():
    global gold
    if selected_index is None:
        result_label.config(text="⚠️ 검을 선택하세요.")
        return

    level = inventory[selected_index]
    cost = upgrade_cost(level)

    if gold < cost:
        result_label.config(text="❌ 골드 부족! 강화 실패.")
        return

    gold -= cost
    roll = random.uniform(0, 100)
    success = roll <= success_rates[level]

    if success:
        level += 1
        inventory[selected_index] = level
        result = "✅ 강화 성공!"
    else:
        if level >= 25:
            inventory[selected_index] = 0
            gold = 500
            result = "💥 검이 폭☆발했다! 모든 것이 사라졌다..."
        elif level >= 20:
            inventory[selected_index] = 0 if random.random() < 0.5 else max(level - 3, 0)
            result = "⚠️ 대실패! 단계 초기화 or 대폭 하락!"
        elif level >= 10:
            inventory[selected_index] = max(level - 2, 0)
            result = "📉 단계 하락!"
        elif level >= 5:
            inventory[selected_index] = max(level - 1, 0)
            result = "📉 약간 하락!"
        else:
            result = "😌 아무 일도 일어나지 않았습니다."

    update_ui()
    result_label.config(text=result)

    if gold <= 0:
        game_over()

def sell_weapon():
    global gold
    if selected_index is None:
        result_label.config(text="⚠️ 검을 선택하세요.")
        return

    level = inventory[selected_index]
    if level <= 3:
        result_label.config(text="🪓 +3 이하 검은 쓰레기입니다. 팔 수 없습니다.")
        return

    price = int((level ** 2.3) * 100)
    gold += price
    result_label.config(text=f"💰 {get_weapon_name(level)} 판매! +{price:,}G")

    del inventory[selected_index]
    update_ui()

def gamble():
    global gold, win_streak

    if gold <= 0:
        game_over()
        return

    mode = simpledialog.askstring("🎰 도박장", "도박 종류 선택:\n1. 안전 (80%, 1.5배)\n2. 고위험 (40%, 2배)\n입력: 1 or 2")
    if not mode or mode not in ['1', '2']:
        return

    bet = simpledialog.askinteger("💸 베팅", f"얼마를 걸겠습니까? (1 ~ {gold})", minvalue=1, maxvalue=gold)
    if bet is None:
        return

    win_chance = 0.8 if mode == '1' else 0.4
    multiplier = 1.5 if mode == '1' else 2

    if random.random() < win_chance:
        winnings = int(bet * multiplier)
        gold += winnings
        win_streak += 1
        result_label.config(text=f"🎉 도박 성공! +{winnings:,}G (연승 {win_streak}회)", fg="green", bg=root.cget("bg"))
    else:
        gold -= bet
        win_streak = 0
        result_label.config(text=f"💥 도박 실패! -{bet:,}G", fg="red", bg="black")
        result_label.after(500, lambda: result_label.config(fg="black", bg=root.cget("bg")))

    update_ui()
    retry_gamble_button.config(state=tk.NORMAL)

    if gold <= 0:
        game_over()

    update_ui()
    retry_gamble_button.config(state=tk.NORMAL)

    if gold <= 0:
        game_over()

def retry_gamble():
    gamble()

# --------- UI ----------
root = tk.Tk()
root.title("강화 지옥 - 인벤토리 시스템")
root.geometry("700x520")  # 가로 넓힘
root.resizable(False, False)

# 좌우 프레임 만들기
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- 기존 UI 위젯들을 left_frame에 넣기 ---
slot_info_label = tk.Label(left_frame, text="", font=("Arial", 11))
slot_info_label.pack()

gold_label = tk.Label(left_frame, text="", font=("Arial", 12))
gold_label.pack(pady=5)

weapon_listbox = tk.Listbox(left_frame, height=6, font=("Arial", 12))
weapon_listbox.pack(pady=5)
weapon_listbox.bind("<<ListboxSelect>>", on_select)

selected_label = tk.Label(left_frame, text="선택된 검 없음", font=("Arial", 12))
selected_label.pack()

cost_label = tk.Label(left_frame, text="💰 강화 비용: -", font=("Arial", 12))
cost_label.pack()

rate_label = tk.Label(left_frame, text="📈 성공 확률: -", font=("Arial", 12))
rate_label.pack()

enhance_button = tk.Button(left_frame, text="🔨 강화하기", font=("Arial", 13), command=enhance)
enhance_button.pack(pady=5)

sell_button = tk.Button(left_frame, text="💰 검 판매", font=("Arial", 13), command=sell_weapon)
sell_button.pack(pady=5)

gamble_button = tk.Button(left_frame, text="🎲 도박장", font=("Arial", 13), command=gamble)
gamble_button.pack(pady=5)

retry_gamble_button = tk.Button(left_frame, text="🔁 다시 도박하기", font=("Arial", 11), command=retry_gamble, state=tk.DISABLED)
retry_gamble_button.pack(pady=5)

add_button = tk.Button(left_frame, text="➕ 새 검 추가", font=("Arial", 12), command=add_weapon)
add_button.pack(pady=5)

expand_button = tk.Button(left_frame, text="📦 슬롯 확장 구매", font=("Arial", 12), command=expand_slot)
expand_button.pack(pady=5)

result_label = tk.Label(left_frame, text="", font=("Arial", 12), fg="red")
result_label.pack(pady=10)

# --- 오른쪽에 게임 설명 및 가격표 넣기 ---
game_explanation = """
🎮 게임 설명

- 검을 강화하여 최고의 무기를 만드세요.
- 강화 단계가 높아질수록 성공 확률이 낮아지고 강화 비용은 증가합니다.
- 인벤토리는 슬롯 수 만큼 검을 보유할 수 있습니다.
- 슬롯 확장 구매로 최대 슬롯을 늘릴 수 있습니다.
- 골드를 모두 잃으면 게임이 종료됩니다.

💰 가격표 및 확률 정보

- 슬롯 확장 비용: (현재 슬롯 + 1) × 10,000G
- 검 판매 가격: 강화 단계에 따라 다름 (+3 이하 검은 판매 불가)
- 강화 비용: 100 + 강화 단계 × 150 G
- 강화 성공 확률: 단계별 성공 확률이 다름 (게임 내 표 참고)
- 도박장 정보:
    1) 안전 도박 - 성공 확률 80%, 보상 1.5배
    2) 고위험 도박 - 성공 확률 40%, 보상 2배
"""

explanation_label = tk.Label(right_frame, text=game_explanation, justify=tk.LEFT, font=("Arial", 12), anchor="nw")
explanation_label.pack(fill=tk.BOTH, expand=True)

update_ui()
root.mainloop()
