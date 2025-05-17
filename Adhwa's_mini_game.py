import streamlit as st
import random

# =============================================================
#  🎓 TEBAK DERET WISUDA  –  KODE ASLI + PENJELASAN PER SECTION
# -------------------------------------------------------------
#  •  HANYA menambahkan komentar agar kamu mudah memahami dan
#     memodifikasi.  Tidak mengubah logika inti.
#  •  Setiap blok diberi header "#####" agar cepat dicari.
# =============================================================

##### 1. KONFIGURASI HALAMAN ###################################
#  * WAJIB dipanggil sebelum perintah Streamlit lain apa pun
st.set_page_config(page_title="Tebak Deret Wisuda", page_icon="🎓", layout="centered")

##### 2. JUDUL & DESKRIPSI ####################################
st.title("🎓 Tebak Deret Wisuda 🎉")
st.write("Jawab dengan tepat untuk membuka ucapan spesial!")

##### 3. DAFTAR POLA (Sulit ➜ Mudah) ###########################
#  patterns = [ (nama, fungsi_pola, deskripsi) ]
#  – Fungsi pola menerima n (1‑based) dan mengembalikan suku ke‑n.
def make_recursive(start, b, c):
    """Mengembalikan fungsi pola rekursif dgn parameter random."""
    def f(n):
        term = start
        for _ in range(n-1):          # hitung sampai suku n
            term = term * b + c
        return term
    return f
# --- parameter random khusus pola rekursif ---
if "patterns" not in st.session_state or st.session_state.new_question:
    suku_pertama = random.randint(1, 20)
    a = random.randint(3, 5)
    b = random.randint(2, 3)
    c = random.randint(1, 3)

    st.session_state.patterns = [
        (f"prev*{b}+{c}", make_recursive(suku_pertama, b, c),
         f"Pola: prev * {b} + {c}"),
        (f"{a}n",  lambda n, a=a: a*n,   f"Pola: prev + {a}"),
        ("2n",     lambda n: 2*n,        "Pola: prev + 2"),
    ]

##### 4. INISIALISASI SESSION_STATE ############################
#  Digunakan Streamlit untuk menyimpan data antar rerun.
if "level" not in st.session_state:           # index pola saat ini
    st.session_state.level = 0
    st.session_state.new_question = True      # trigger generate ulang

if "u" not in st.session_state:              # suku ke‑berapa yang hilang
    st.session_state.u = None
if "answer" not in st.session_state:         # jawaban benar
    st.session_state.answer = None
if "sequence" not in st.session_state:       # list deret (tanpa ?)
    st.session_state.sequence = None

# Perubahan
if "hint_shown" not in st.session_state:   # apakah deskripsi pola sudah ditampakkan?
    st.session_state.hint_shown = False
# Perubahan

##### 5. FUNGSI BUAT PERTANYAAN BARU ###########################
#  1. Pilih pola sesuai level
#  2. Pilih indeks u (4‑7)
#  3. Hitung deret sampai suku u‑1 → sequence
#  4. Simpan jawaban suku ke‑u
#  5. Set new_question = False

def generate_question():
    pattern_name, f, _ = st.session_state.patterns[st.session_state.level]
    u = random.randint(4, 7)                 # suku yang akan disembunyikan
    seq = [f(n) for n in range(1, u)]        # deret sampai sebelum u
    ans = f(u)                               # nilai suku ke‑u

    # simpan di session_state
    st.session_state.u = u
    st.session_state.sequence = seq
    st.session_state.answer = ans
    st.session_state.new_question = False

##### 6. GENERATE PERTANYAAN JIKA PERLU ########################
if st.session_state.new_question:
    generate_question()

##### 7. TAMPILKAN PERTANYAAN #################################
total_lv = len(st.session_state.patterns)                      
display_lv = total_lv - st.session_state.level

# pattern_name, _, pattern_desc = patterns[st.session_state.level]
# st.subheader(f"Level {display_lv} •    {pattern_desc}")
_, _, pattern_desc = st.session_state.patterns[st.session_state.level]
desc_to_show = pattern_desc if st.session_state.hint_shown else " 🔒  Hint"
st.subheader(f"Level {display_lv} • {desc_to_show}")

deret_display = ", ".join(map(str, st.session_state.sequence)) + ", ?"
st.write(f"Tebak **suku ke-{st.session_state.u}** dari deret berikut:")
st.code(deret_display)

# Perubahan
if "feedback" in st.session_state:
    kind, msg = st.session_state.feedback
    if kind in {"success", "error"}:          # tampilkan hanya 2 jenis
        {"success": st.success,
         "error":   st.error}[kind](msg)
    del st.session_state.feedback             # hapus agar tampil sekali
# if "feedback" in st.session_state:
#     kind, msg = st.session_state.feedback
#     {"success": st.success, "error": st.error}[kind](msg)
#     del st.session_state.feedback
# Perubahan

##### 8. INPUT JAWABAN USER ###################################
user_input = st.text_input("Jawabanmu (angka bulat):", key="answer_input")

#perubahan
# col_submit, col_new = st.columns([1, 1])
col_submit, col_new, col_hint = st.columns([1, 1, 1])

with col_submit:
    submit_clicked = st.button(
        "Kirim",              # ganti label kalau mau
        type="primary",
        use_container_width=True
    )

with col_new:
    pola_clicked = st.button(
        "Pola Baru 🔄",
        use_container_width=True
    )

with col_hint:
    hint_clicked = st.button(
        "Hint 🗝️",
        use_container_width=True
    )
#perubahan

##### 9. LOGIKA TOMBOL SUBMIT #################################

if submit_clicked:
    try:
        guess = int(user_input.strip())
        if guess == st.session_state.answer:
            st.success("Yowwww! Jawabanmu benaaar 🎉")
            st.balloons()
            # --- Ganti ucapan di bawah sesuai keinginan ---
            st.markdown("**Adhwaaaa, selamat wisudaa! Semoga selalu diberi kemudahan di semua jalan yang dipilih, yaa!!. 🌌**")
            if st.button("Main Lagi", type="secondary"):
                st.session_state.level = 0
                st.session_state.new_question = True
                st.session_state.hint_shown = False
                st.rerun()
        else:
            st.error("Ups, belum tepat!")                 # tampil segera
            st.session_state.feedback = ("error", "Ups, belum tepat!")
            # Naikkan level, tapi jangan sampai keluar indeks
            if st.session_state.level + 1 >= len(st.session_state.patterns):
                st.session_state.level = 0               # atau bisa tampilkan game-over
            else:
                st.session_state.level += 1
            st.session_state.new_question = True
            st.session_state.hint_shown = False
            st.rerun()
            # st.error("Ups, belum tepat!")
            # st.session_state.level += 1
            # st.session_state.new_question = True
            # st.session_state.hint_shown = False
            # st.rerun() 
            # if st.session_state.level >= len(patterns):
            #     st.warning("Game over... tapi tetap semangat! Klik untuk coba lagi.")
            #     if st.button("Coba Lagi"):
            #         st.session_state.level = 0
            #         st.session_state.new_question = True
            #         st.rerun()
            # else:
            #     st.session_state.new_question = True
            #     st.rerun()
    except ValueError:
        st.error("Masukkan angka bulat yaa!")

if pola_clicked:
    st.session_state.new_question = True
    st.session_state.hint_shown = False
    st.session_state.feedback = ("info", "")    # hapus pesan lama
    st.rerun()

if hint_clicked:
    st.session_state.hint_shown = True      # tampilkan deskripsi pola
    st.rerun()
