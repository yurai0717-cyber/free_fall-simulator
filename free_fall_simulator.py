import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="자유낙하/수평 투사 시뮬레이터", layout="wide")
st.title("🌎 자유낙하/수평 투사 시뮬레이터 (위치 표시 포함)")

# ----- 사이드바 설정 -----
st.sidebar.header("실험 조건 설정")

planet = st.sidebar.selectbox("천체 선택", ["지구", "달"])
g = 9.8 if planet == "지구" else 1.6

air_resistance = st.sidebar.checkbox("공기 저항 포함", value=False)

mass1 = st.sidebar.slider("공 1 질량 (kg)", 0.1, 10.0, 1.0, 0.1)
mass2 = st.sidebar.slider("공 2 질량 (kg)", 0.1, 10.0, 2.0, 0.1)

h0 = st.sidebar.number_input("초기 높이 (m)", 5.0, 100.0, 20.0, 1.0)
dt = 0.05
t_max = 5.0

motion_type = st.sidebar.selectbox("운동 유형", ["자유낙하", "수평 투사"])
vx1 = st.sidebar.number_input("공 1 수평 속도 (m/s)", 0.0, 20.0, 0.0, 0.1)
vx2 = st.sidebar.number_input("공 2 수평 속도 (m/s)", 0.0, 20.0, 0.0, 0.1)

# 마커 간격 설정
marker_interval = st.sidebar.slider("공 위치 표시 간격 (초)", 0.05, 1.0, 0.2, 0.05)

run_sim = st.sidebar.button("▶ 시뮬레이션 실행")

# ----- 공 위치 계산 -----
def simulate_motion(m, g, air=False, h0=10, vx=0, dt=0.05, t_max=5.0):
    t = np.arange(0, t_max, dt)
    y = np.zeros_like(t)
    x = np.zeros_like(t)
    y[0] = h0
    x[0] = 0
    vy = 0
    k = 0.05  # 공기 저항 계수

    for i in range(1, len(t)):
        ay = -g
        if air:
            ay -= (k / m) * vy * abs(vy)
        vy += ay * dt
        y[i] = y[i-1] + vy*dt
        x[i] = x[i-1] + vx*dt
        if y[i] < 0:
            y[i] = 0
            y[i+1:] = 0
            x[i+1:] = x[i]
            break
    return t, x, y

# ----- 애니메이션 -----
if run_sim:
    st.write(f"🌕 천체: **{planet}**, 중력가속도 g = {g:.1f} m/s²")
    st.write(f"💡 두 공의 이동과 {marker_interval}초마다 위치 표시를 보여줍니다.")

    t, x1, y1 = simulate_motion(mass1, g, air_resistance, h0, vx1, dt, t_max)
    _, x2, y2 = simulate_motion(mass2, g, air_resistance, h0, vx2, dt, t_max)

    placeholder = st.empty()
    fig, ax = plt.subplots(figsize=(6, 6))
    max_x = max(max(x1), max(x2)) + 1
    ax.set_xlim(-1, max_x)
    ax.set_ylim(0, h0 + 2)
    ax.set_xlabel("x 위치 (m)")
    ax.set_ylabel("높이 (m)")
    ax.set_title("공 이동 애니메이션")
    ball1, = ax.plot([x1[0]], [y1[0]], 'ro', markersize=15, label=f"공1 ({mass1}kg)")
    ball2, = ax.plot([x2[0]], [y2[0]], 'bo', markersize=15, label=f"공2 ({mass2}kg)")
    trail1, = ax.plot([], [], 'r--', alpha=0.5)
    trail2, = ax.plot([], [], 'b--', alpha=0.5)
    ax.legend()

    for i in range(len(t)):
        # 공 이동
        ball1.set_data([x1[i]], [y1[i]])
        ball2.set_data([x2[i]], [y2[i]])
        # 궤적
        trail1.set_data(x1[:i+1], y1[:i+1])
        trail2.set_data(x2[:i+1], y2[:i+1])
        # marker_interval마다 위치 표시
        if i % int(marker_interval / dt) == 0:
            ax.plot([x1[i]], [y1[i]], 'ro', markersize=8, alpha=0.7)
            ax.plot([x2[i]], [y2[i]], 'bo', markersize=8, alpha=0.7)
        placeholder.pyplot(fig)
        time.sleep(dt)
else:
    st.info("▶ 왼쪽 사이드바의 **'시뮬레이션 실행' 버튼**을 눌러 시작하세요.")
