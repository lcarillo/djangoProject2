import pandas as pd
import requests
from io import StringIO

def baixar_e_salvar_csv():
    url = "https://aplicacoes.mds.gov.br/sagi/servicos/misocial?fq=anomes_s:2023*&wt=csv&omitHeader=true&fq=cadunico_tot_fam_i:{0%20TO%20*]&q=*&fl=ibge:codigo_ibge,anomes:anomes_s,cadunico_tot_fam:cadunico_tot_fam_i,cadunico_tot_pes:cadunico_tot_pes_i,cadunico_tot_fam_rpc_ate_meio_sm:cadunico_tot_fam_rpc_ate_meio_sm_i,cadunico_tot_pes_rpc_ate_meio_sm:cadunico_tot_pes_rpc_ate_meio_sm_i,cadunico_tot_fam_pob:cadunico_tot_fam_pob_i,cadunico_tot_pes_pob:cadunico_tot_pes_pob_i,cadunico_tot_fam_ext_pob:cadunico_tot_fam_ext_pob_i,cadunico_tot_pes_ext_pob:cadunico_tot_pes_ext_pob_i,cadunico_tot_fam_pob_e_ext_pob:cadunico_tot_fam_pob_e_ext_pob_i,cadunico_tot_pes_pob_e_ext_pob:cadunico_tot_pes_pob_e_ext_pob_i&rows=100000000&sort=anomes_s%20desc,%20codigo_ibge%20asc"
    response = requests.get(url)
    df = pd.read_csv(StringIO(response.text), header=None)

    df.columns = [
        "IBGE", "AnoMês", "Famílias Total", "Pessoas Total",
        "Famílias até 1/2 SM", "Pessoas até 1/2 SM",
        "Famílias Pobres", "Pessoas Pobres",
        "Famílias Ext. Pobres", "Pessoas Ext. Pobres",
        "Famílias Pobres e Ext.", "Pessoas Pobres e Ext."
    ]

    df.to_csv("cadunico_2023.csv", index=False)
