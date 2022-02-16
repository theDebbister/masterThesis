#!/bin/bash
## already trained long
# eng_latn_uk_broad_filtered eng_latn_uk_narrow eng_latn_us_broad_filtered eng_latn_us_narrow fra_latn_broad_filtered ell_grek_broad_filtered cmn_hani_broad deu_latn_broad_filtered deu_latn_narrow eus_latn_broad fin_latn_broad 



# --valid "data/$LANG.dict.part.dev" --test "data/$LANG.dict.part.test" 

for LANG in fin_latn_narrow ind_latn_broad ind_latn_narrow kat_geor_broad_filtered mya_mymr_broad_filtered rus_cyrl_narrow spa_latn_ca_broad_filtered spa_latn_ca_narrow spa_latn_la_broad_filtered kor_hang_narrow_filtered jpn_hira_narrow_filtered spa_latn_la_narrow tgl_latn_broad tgl_latn_narrow tha_thai_broad tur_latn_broad tur_latn_narrow_filtered hin_deva_broad_filtered hin_deva_narrow zul_latn_broad vie_latn_hanoi_narrow_filtered; do
  g2p-seq2seq --train "feature_data/${LANG}_FEATURES_v2.tsv" --model_dir "features_models/${LANG}_v2" &>> log_FEATURES/${LANG}_long.txt
done;


