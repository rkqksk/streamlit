import streamlit as st
import sqlite3
import os
from github import Github

# GitHub 레포지토리 정보
repo_owner = "rkqksk"
repo_name = "streamlit"
branch_name = "main"

# 데이터베이스 파일 경로 및 파일 이름
db_file_path = "data/work_log.db"

# 데이터베이스 연결 함수
def connect_db():
    conn = sqlite3.connect(db_file_path)
    return conn

# 데이터베이스 생성 함수
def create_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            task TEXT NOT NULL,
            hours INTEGER NOT NULL,
            notes TEXT
        );
    """)

    conn.commit()
    conn.close()

# 작업일지 작성 함수
def create_work_log():
    st.header("Create Work Log")

    date = st.date_input("Date")
    task = st.text_input("Task")
    hours = st.number_input("Hours", min_value=0, max_value=24, step=1)
    notes = st.text_area("Notes")

    if st.button("Submit"):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO work_log (date, task, hours, notes)
            VALUES (?, ?, ?, ?)
        """, (str(date), task, hours, notes))

        conn.commit()
        conn.close()

        st.success("Work log created successfully!")

        # 데이터베이스 파일을 GitHub 리포지토리에 자동으로 커밋하여 저장
        try:
            # GitHub API 인증
            access_token = st.secrets["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"]
            g = Github(access_token)

            # 리포지토리 가져오기
            repo = g.get_user(rkqksk).get_repo(streamlit)

            # 파일 커밋
            with open(db_file_path, "rb") as file:
                content = file.read()
                repo.create_file(db_file_path, "work log created", content, branch=branch_name)

            st.success("Work log saved to GitHub successfully!")
        except Exception as e:
            st.error("Failed to save work log to GitHub!")
            st.error(e)

# 앱 실행
if __name__ == "__main__":
    st.set_page_config(page_title="Work Log App")

    # 데이터베이스 생성
    if not os.path.exists(db_file_path):
        create_db()

    # 작업일지 작성
    create_work_log()
