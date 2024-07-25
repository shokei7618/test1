#
# Darts メイン処理
#
import streamlit as st

import darts.config_view as cv
import darts.login_view as lv
import darts.main_view as mv
from darts.const import VERSION
from darts.darts_alm_list import DartsAlmList
from darts.darts_alm_list_sa import DartsAlmListSA
from darts.darts_data_his_enb import DartsDataHisEnb
from darts.darts_data_his_gnb import DartsDataHisGnb
from darts.session_state_manager import SessionStateManager
from darts.streamlit_login import Authenticate

session_state = SessionStateManager()


def render_help():
    """オンラインヘルプ表示"""
    cols = st.columns([2, 28])
    with cols[0]:
        with open("images/darts_logo.svg", "r") as img:
            st.image(img.read(), width=64)
    with cols[1]:
        with open("README.md", "r", encoding="utf-8") as f:
            st.markdown(f.read())


##########################################################################################
def main():
    """メイン関数 ログイン状態を確認して画面を切り替える"""
    st.set_page_config(layout="wide", page_title="Darts", page_icon="images/darts_logo.svg")  # ワイド表示

    # URLのパラメータに?targetがあれば、Darts内のダッシュボードを表示
    if "target" in st.query_params:
        target = st.query_params.target
        if target == "help":
            render_help()
            return

        # 認証情報をcookieから取得
        if session_state.auth is None:
            session_state.auth = Authenticate("m_cat_darts", "m_cat_darts_sig", cookie_expiry_days=7)
        if session_state.auth.cookie_login():
            session_state.user = session_state.auth.username
            session_state.passwd = session_state.auth.password
        else:
            # 関数が2回呼び出される。1回目はcookieを取得できないのでreturn
            return

        if target == "darts_data_his_enb":
            DartsDataHisEnb()
        elif target == "darts_data_his_gnb":
            DartsDataHisGnb()
        elif target == "darts_alm_list":
            DartsAlmList()
        elif target == "darts_alm_list_sa":
            DartsAlmListSA()
        elif target == "dashboard_config":
            cv.render_dashboard_config(st.query_params.node)
    else:
        with st.sidebar:
            with open("images/darts_logo.svg", "r") as img:
                st.image(img.read(), width=128)

            st.header(":snowflake: Darts(:red[da]shboa:red[r]d :red[t]ran:red[s]fer​)")

        if not session_state.login:
            cv.init_settings()
            lv.render_login_view()  # 未ログインの場合はログイン画面を表示
            render_help()
        else:
            mv.render_main_view()  # ログイン済みの場合はメイン画面を表示
            with st.sidebar:
                st.divider()
                cv.render_settings()  # 設定
                lv.render_logout_button("ログアウト")

        with st.sidebar:
            st.markdown("[Dartsの使い方](?target=help)")
            st.markdown(
                "お問い合わせ先(Slack): [#si-x-darts-community](https://docomo.enterprise.slack.com/archives/C06AALPEY79)"
            )
            st.write(VERSION)


if __name__ == "__main__":
    main()
