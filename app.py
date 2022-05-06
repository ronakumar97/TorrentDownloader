import libtorrent as lt
import time
import streamlit as st

def run_method(user_input):
    ses = lt.session()
    ses.listen_on(6881, 6891)
    params = {
        'storage_mode': lt.storage_mode_t(2)}

    link = user_input
    handle = lt.add_magnet_uri(ses, link, params)
    ses.start_dht()

    print('downloading metadata...')
    while (not handle.has_metadata()):
        time.sleep(1)
    print('got metadata, starting torrent download...')
    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                     'downloading', 'finished', 'seeding', 'allocating']
        print('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
              (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
               s.num_peers, state_str[s.state]))
        time.sleep(5)

def main():
    st.title('Torrent Downloader Web App')

    with st.form(key='my_form'):
        user_input = st.text_input(label='Magnet Link', placeholder="magnet:?", value="")

        submit_button = st.form_submit_button(label='Submit')
        if (submit_button):
            run_method(user_input)

if __name__ == '__main__':
    main()