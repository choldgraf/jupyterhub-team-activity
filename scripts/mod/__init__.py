from glob import glob
import os.path as op
import os
from watchtower import comments_
import pandas as pd
import altair as alt

def list_data(watchtower_dir='~/watchtower_data'):
    all_data = []
    for folder in glob(op.join(op.expanduser(watchtower_dir), '*', '*')):
        org, repo = folder.split(op.expanduser(watchtower_dir))[-1].strip(os.sep).split(os.sep)[:2]
        data = comments_.load_comments(org, repo)
        date_col = 'created_at' if 'created_at' in data.columns else 'date'
        data = data[[date_col]].resample('Y', on=date_col).count()
        data['org'] = org
        data['repo'] = repo
        all_data.append(data.rename(columns={'created_at': 'count'}))
    all_data = pd.concat(all_data).set_index(['org', 'repo'], append=True)['count'].unstack('created_at')
    all_data.columns = all_data.columns.year
    return all_data


def delete_data(org, repo, data_dir='~/watchtower_data'):
    path_data = op.join(op.expanduser(data_dir), org, repo)
    if op.exists(path_data):
        sh.rmtree(path_data)
        print('Deleted {}/{}'.format(org, repo))

        
# Data
hub_projects = {'jupyter': ['repo2docker'],
                'jupyterhub': ['zero-to-jupyterhub-k8s', 'the-littlest-jupyterhub', 'jupyterhub',
                               'binderhub', 'binder', 'team-compass', 'mybinder.org-deploy',
                               'configurable-http-proxy', 'nativeauthenticator', 'traefik-proxy',
                               'jupyter-server-proxy']}