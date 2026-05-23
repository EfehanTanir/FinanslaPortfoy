import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Efsane Portföyler | Finansla.net", layout="wide", page_icon="💼", initial_sidebar_state="collapsed")

st.title("💼 Finansla.net | Efsane Yatırımcı Portföyleri")
st.caption("Dünyanın en başarılı yatırımcılarının portföylerini incele, kendi portföyünle ve piyasa endeksleriyle karşılaştır.")
st.markdown("---")

# --- EFSANE PORTFÖYLER ---
PORTFOYLER = {
    "Warren Buffett 🐂": {
        "aciklama": "Değer yatırımcılığının ustası. Uzun vadeli, güçlü markalı şirketlere odaklanır.",
        "hisseler": {
            "AAPL": 44.0, "BAC": 10.0, "AXP": 8.5, "KO": 7.0,
            "CVX": 6.5, "OXY": 5.0, "MCO": 4.0, "KHC": 3.5,
            "DVA": 3.0, "USB": 2.5, "OTHER": 6.0
        }
    },
    "Ray Dalio 🌊": {
        "aciklama": "All Weather Portfolio: Her ekonomik koşulda çalışacak şekilde tasarlanmış.",
        "hisseler": {
            "SPY": 30.0, "TLT": 40.0, "IEF": 15.0, "GLD": 7.5, "DBC": 7.5
        }
    },
    "Peter Lynch 📈": {
        "aciklama": "Magellan Fund efsanesi. Büyüme + değer karışımı, günlük hayattan hisse seçer.",
        "hisseler": {
            "MSFT": 15.0, "JNJ": 12.0, "PG": 10.0, "WMT": 10.0,
            "MCD": 8.0, "DIS": 8.0, "NKE": 7.0, "SBUX": 7.0,
            "HD": 7.0, "TGT": 6.0, "OTHER": 10.0
        }
    },
    "George Soros 🌍": {
        "aciklama": "Makro yatırımcı. Küresel ekonomik trendlere göre büyük bahisler oynar.",
        "hisseler": {
            "NVDA": 18.0, "MSFT": 12.0, "AMZN": 10.0, "GOOGL": 8.0,
            "META": 8.0, "TSM": 7.0, "ORCL": 7.0, "PLTR": 6.0,
            "UPS": 5.0, "OTHER": 19.0
        }
    },
    "Michael Burry 🔍": {
        "aciklama": "The Big Short'un kahramanı. Değer altında kalmış, gözden kaçmış fırsatları arar.",
        "hisseler": {
            "BABA": 20.0, "JD": 15.0, "PDD": 12.0, "HCA": 10.0,
            "CVS": 10.0, "ORCL": 8.0, "MGM": 8.0, "OTHER": 17.0
        }
    },
    "Cathie Wood 🚀": {
        "aciklama": "ARK Invest kurucusu. Yapay zeka, genomik, fintech gibi disruptif teknolojilere odaklanır.",
        "hisseler": {
            "TSLA": 25.0, "COIN": 10.0, "ROKU": 8.0, "PLTR": 7.0,
            "CRSP": 6.0, "SQ": 6.0, "SHOP": 6.0, "PATH": 5.0,
            "TWLO": 5.0, "OTHER": 22.0
        }
    },
    "Charlie Munger 🧠": {
        "aciklama": "Buffett'ın ortağı. Kaliteli iş modellerine, geniş hendekli şirketlere yatırım yapar.",
        "hisseler": {
            "BABA": 30.0, "BAC": 20.0, "USB": 15.0, "BK": 15.0,
            "POSCO": 10.0, "OTHER": 10.0
        }
    },
    "Stanley Druckenmiller 💡": {
        "aciklama": "Soros'un eski ortağı. Makro trendleri takip eder, esnek ve dinamik portföy yönetir.",
        "hisseler": {
            "NVDA": 20.0, "MSFT": 15.0, "META": 10.0, "GOOGL": 10.0,
            "AMZN": 10.0, "CRH": 8.0, "NOG": 7.0, "OTHER": 20.0
        }
    }
}

KARSILASTIRMALAR = {
    "BIST 100": "XU100.IS",
    "S&P 500": "SPY",
    "Altın": "GLD",
    "Nasdaq": "QQQ",
    "Dolar/TL": "TRY=X"
}

# --- FONKSİYONLAR ---
@st.cache_data(ttl=300)
def get_fiyat(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        fiyat = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('navPrice')
        if not fiyat:
            hist = t.history(period="1d")
            fiyat = hist['Close'].iloc[-1] if not hist.empty else None
        return round(fiyat, 2) if fiyat else None
    except:
        return None

@st.cache_data(ttl=300)
def get_yillik_getiri(ticker, yil=1):
    try:
        bitis = datetime.now()
        baslangic = bitis - timedelta(days=365 * yil)
        t = yf.Ticker(ticker)
        hist = t.history(start=baslangic, end=bitis)
        if hist.empty or len(hist) < 2:
            return None
        getiri = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
        return round(getiri, 2)
    except:
        return None

@st.cache_data(ttl=300)
def get_grafik_verisi(ticker, yil=1):
    try:
        bitis = datetime.now()
        baslangic = bitis - timedelta(days=365 * yil)
        t = yf.Ticker(ticker)
        hist = t.history(start=baslangic, end=bitis)
        if hist.empty:
            return None
        hist['Normalize'] = (hist['Close'] / hist['Close'].iloc[0]) * 100
        return hist
    except:
        return None

# --- ANA SEKME YAPISI ---
tab1, tab2, tab3 = st.tabs(["🏆 Efsane Portföyler", "📊 Karşılaştırma", "🎯 Kendi Portföyüm"])

# ==================== TAB 1: EFSANE PORTFÖYLER ====================
with tab1:
    secilen_efsane = st.selectbox("Yatırımcı Seç", list(PORTFOYLER.keys()))
    portfoy = PORTFOYLER[secilen_efsane]

    st.info(f"**{secilen_efsane}** — {portfoy['aciklama']}")

    hisseler = {k: v for k, v in portfoy["hisseler"].items() if k != "OTHER"}
    other = portfoy["hisseler"].get("OTHER", 0)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Portföy Dağılımı")
        satirlar = []
        for hisse, agirlik in hisseler.items():
            fiyat = get_fiyat(hisse)
            yillik = get_yillik_getiri(hisse)
            satirlar.append({
                "Hisse": hisse,
                "Ağırlık (%)": f"%{agirlik}",
                "Güncel Fiyat": f"${fiyat}" if fiyat else "—",
                "1Y Getiri": f"%{yillik:.1f}" if yillik else "—"
            })
        if other > 0:
            satirlar.append({"Hisse": "DİĞER", "Ağırlık (%)": f"%{other}", "Güncel Fiyat": "—", "1Y Getiri": "—"})

        df = pd.DataFrame(satirlar)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col2:
        st.subheader("🥧 Ağırlık Dağılımı")
        labels = list(hisseler.keys()) + (["DİĞER"] if other > 0 else [])
        values = list(hisseler.values()) + ([other] if other > 0 else [])
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, values=values,
            hole=0.4,
            textinfo='label+percent'
        )])
        fig_pie.update_layout(
            template="plotly_dark",
            showlegend=False,
            height=400,
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Yıllık performans grafiği
    st.subheader("📈 Portföy Performansı (Normalize, 1 Yıl)")
    fig_line = go.Figure()
    renkler = ["#00d4ff", "#ff6b6b", "#51cf66", "#ffd43b", "#cc5de8", "#ff922b", "#74c0fc"]
    for i, (hisse, _) in enumerate(hisseler.items()):
        veri = get_grafik_verisi(hisse)
        if veri is not None:
            fig_line.add_trace(go.Scatter(
                x=veri.index, y=veri['Normalize'],
                name=hisse,
                line=dict(color=renkler[i % len(renkler)], width=1.5)
            ))
    fig_line.update_layout(
        template="plotly_dark", height=400,
        yaxis_title="Başlangıç = 100",
        hovermode="x unified"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ==================== TAB 2: KARŞILAŞTIRMA ====================
with tab2:
    st.subheader("📊 Efsaneler vs Piyasa Endeksleri")

    yil_secim = st.radio("Zaman Aralığı", ["1 Yıl", "3 Yıl", "5 Yıl"], horizontal=True)
    yil_map = {"1 Yıl": 1, "3 Yıl": 3, "5 Yıl": 5}
    secilen_yil = yil_map[yil_secim]

    with st.spinner("Veriler yükleniyor..."):
        karsilastirma_verisi = []

        # Efsanelerin ana hisselerinin ağırlıklı getirisi
        for isim, portfoy in PORTFOYLER.items():
            hisseler = {k: v for k, v in portfoy["hisseler"].items() if k != "OTHER"}
            toplam_agirlik = sum(hisseler.values())
            agirlikli_getiri = 0
            veri_sayisi = 0
            for hisse, agirlik in hisseler.items():
                getiri = get_yillik_getiri(hisse, secilen_yil)
                if getiri:
                    agirlikli_getiri += (agirlik / toplam_agirlik) * getiri
                    veri_sayisi += 1
            if veri_sayisi > 0:
                karsilastirma_verisi.append({
                    "İsim": isim,
                    "Getiri (%)": round(agirlikli_getiri, 1),
                    "Tür": "Efsane"
                })

        # Endeksler
        for isim, ticker in KARSILASTIRMALAR.items():
            getiri = get_yillik_getiri(ticker, secilen_yil)
            if getiri:
                karsilastirma_verisi.append({
                    "İsim": isim,
                    "Getiri (%)": round(getiri, 1),
                    "Tür": "Endeks"
                })

    if karsilastirma_verisi:
        df_karsi = pd.DataFrame(karsilastirma_verisi).sort_values("Getiri (%)", ascending=True)

        renkler_bar = ["#00d4ff" if t == "Efsane" else "#ffd43b" for t in df_karsi["Tür"]]

        fig_bar = go.Figure(go.Bar(
            x=df_karsi["Getiri (%)"],
            y=df_karsi["İsim"],
            orientation='h',
            marker_color=renkler_bar,
            text=[f"%{v:.1f}" for v in df_karsi["Getiri (%)"]],
            textposition='outside'
        ))
        fig_bar.update_layout(
            template="plotly_dark",
            height=500,
            xaxis_title=f"{secilen_yil} Yıllık Getiri (%)",
            margin=dict(l=10, r=60)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.caption("🔵 Mavi = Efsane Yatırımcı &nbsp;&nbsp; 🟡 Sarı = Piyasa Endeksi")

# ==================== TAB 3: KENDİ PORTFÖYÜm ====================
with tab3:
    st.subheader("🎯 Kendi Portföyünü Gir")
    st.info("Hisse sembolü ve ağırlığını gir, efsaneler ve piyasayla karşılaştır.")

    if "portfoy_satirlari" not in st.session_state:
        st.session_state.portfoy_satirlari = [{"hisse": "THYAO.IS", "agirlik": 50}, {"hisse": "GARAN.IS", "agirlik": 50}]

    satirlar = st.session_state.portfoy_satirlari
    yeni_satirlar = []

    for i, satir in enumerate(satirlar):
        c1, c2, c3 = st.columns([2, 1, 0.5])
        with c1:
            hisse = st.text_input(f"Hisse {i+1}", satir["hisse"], key=f"hisse_{i}")
        with c2:
            agirlik = st.number_input(f"Ağırlık % {i+1}", 0.0, 100.0, float(satir["agirlik"]), key=f"agirlik_{i}")
        with c3:
            st.write("")
            st.write("")
            if st.button("❌", key=f"sil_{i}") and len(satirlar) > 1:
                continue
        yeni_satirlar.append({"hisse": hisse, "agirlik": agirlik})

    st.session_state.portfoy_satirlari = yeni_satirlar

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("➕ Hisse Ekle"):
            st.session_state.portfoy_satirlari.append({"hisse": "", "agirlik": 0})
            st.rerun()

    toplam = sum(s["agirlik"] for s in st.session_state.portfoy_satirlari)
    if abs(toplam - 100) > 0.1:
        st.warning(f"⚠️ Toplam ağırlık: %{toplam:.1f} — 100 olmalı")
    else:
        st.success(f"✅ Toplam: %{toplam:.1f}")

    if st.button("🚀 Analizi Başlat", type="primary"):
        with st.spinner("Portföyün analiz ediliyor..."):
            st.markdown("---")
            st.subheader("📊 Portföy Karşılaştırması (1 Yıllık Getiri)")

            # Kullanıcı portföyü getirisi
            gecerli = [(s["hisse"], s["agirlik"]) for s in st.session_state.portfoy_satirlari if s["hisse"] and s["agirlik"] > 0]
            toplam_agirlik = sum(a for _, a in gecerli)
            kullanici_getiri = 0
            for hisse, agirlik in gecerli:
                getiri = get_yillik_getiri(hisse)
                if getiri:
                    kullanici_getiri += (agirlik / toplam_agirlik) * getiri

            karsi_data = [{"İsim": "🎯 Senin Portföyün", "Getiri (%)": round(kullanici_getiri, 1), "Tür": "Sen"}]

            # Efsaneler
            for isim, portfoy in PORTFOYLER.items():
                hisseler = {k: v for k, v in portfoy["hisseler"].items() if k != "OTHER"}
                tot = sum(hisseler.values())
                getiri = 0
                n = 0
                for h, a in hisseler.items():
                    g = get_yillik_getiri(h)
                    if g:
                        getiri += (a / tot) * g
                        n += 1
                if n > 0:
                    karsi_data.append({"İsim": isim, "Getiri (%)": round(getiri, 1), "Tür": "Efsane"})

            # Endeksler
            for isim, ticker in KARSILASTIRMALAR.items():
                g = get_yillik_getiri(ticker)
                if g:
                    karsi_data.append({"İsim": isim, "Getiri (%)": round(g, 1), "Tür": "Endeks"})

            df_son = pd.DataFrame(karsi_data).sort_values("Getiri (%)", ascending=True)

            renk_map = {"Sen": "#51cf66", "Efsane": "#00d4ff", "Endeks": "#ffd43b"}
            renkler_son = [renk_map[t] for t in df_son["Tür"]]

            fig_son = go.Figure(go.Bar(
                x=df_son["Getiri (%)"],
                y=df_son["İsim"],
                orientation='h',
                marker_color=renkler_son,
                text=[f"%{v:.1f}" for v in df_son["Getiri (%)"]],
                textposition='outside'
            ))
            fig_son.update_layout(
                template="plotly_dark",
                height=600,
                xaxis_title="1 Yıllık Getiri (%)",
                margin=dict(l=10, r=60)
            )
            st.plotly_chart(fig_son, use_container_width=True)

            # Sıralama
            sira = df_son[df_son["İsim"] == "🎯 Senin Portföyün"].index
            if not sira.empty:
                sira_no = len(df_son) - df_son.index.get_loc(sira[0])
                st.markdown(f"### Senin portföyün {len(df_son)} katılımcı arasında **{sira_no}. sırada!**")

            st.caption("🟢 Yeşil = Senin Portföyün &nbsp;&nbsp; 🔵 Mavi = Efsane &nbsp;&nbsp; 🟡 Sarı = Endeks")

# Footer
st.markdown("---")
st.caption("© 2025 Finansla.net | Veriler yfinance üzerinden çekilmektedir. Yatırım tavsiyesi değildir.")
