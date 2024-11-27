import os
from tqdm import tqdm
from DrissionPage import Chromium

# https://nomads.ncep.noaa.gov/
for dt in ['20241125']:  # '20241029',
    # 预测批次：实际不用这么多批次，只用00就够了
    for cc in ['00', '06', '12', '18']:  #
        # 原始文件下载后存放位置
        download_dir = "{}/{}".format(dt, cc)  # prefs中指定的目录
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        browser = Chromium().latest_tab
        browser.set.download_path(download_dir)
        for i in tqdm(range(48), desc='进度'):
            fff = '0' * (3 - len(str(i))) + str(i)
            file_name = 'gfs.t{cc}z.pgrb2.0p25.f{fff}'.format(cc=cc, fff=fff)
            # # 下载文件的标准地址
            url_p = r'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs.{dt}%2F{cc}%2Fatmos&file={file_name}&all_var=on&all_lev=on&subregion=&toplat=41&leftlon=110&rightlon=115&bottomlat=34'
            url = url_p.format(dt=dt, cc=cc, file_name=file_name)
            if not os.path.exists(os.path.join(download_dir, file_name)):
                browser.get(url)
            else:
                pass

import pandas as pd
import pygrib as pg
import numpy as np

file_csv_dir = 'data'
for dt in ['20241125']:  # ,'20240927','20240922'
    for cc in ['00', '06', '12', '18']:  #
        # 原始文件存放位置
        download_dir = "{}/{}".format(dt, cc)
        for file in os.listdir(download_dir):
            g = pg.open(os.path.join(download_dir, file))
            leng = len(g.message(1).latitudes)
            data = pd.DataFrame({'latitudes': g.message(1).latitudes, 'longitudes': g.message(1).longitudes,
                                 'p_date': [dt + '_' + cc] * leng,
                                 'ValidDate': [g.message(1).validDate] * leng})
            data_arr = []
            columns_list = []
            for m in g:
                columns_list.append(m.name + str(m.level))
                b = [str(i[0]) for i in m.values.reshape(-1, 1)]
                data_arr.append([str(i[0]) for i in m.values.reshape(-1, 1)])
                # data[m.name + str(m.level)] = m.values.reshape(-1, 1)
            b = np.array(data_arr).T
            new_data = pd.DataFrame(np.array(data_arr).T, columns=columns_list)
            data_set = pd.concat([data, new_data], axis=1)
            g.close()
        # data_set = pd.concat(data_set_list, axis=0)
        data_set.to_csv(os.path.join(file_csv_dir, '{}_{}_fcst.csv'.format(dt, cc)), index=False)
        print(dt, cc, data_set.shape)
