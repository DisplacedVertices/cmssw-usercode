listOfSystematics="
nom
bcjet_up
bcjet_down
ljet_up
ljet_down
"
for syst_var in $listOfSystematics;
do
  echo "starting ${syst_var}"
  python calculate_btag_efficiency.py 2017 3 ${syst_var}
  python calculate_btag_efficiency.py 2017 4 ${syst_var}
  python calculate_btag_efficiency.py 2017 5 ${syst_var}
  python calculate_btag_efficiency.py 2017 7 ${syst_var}
  python presel_btag_efficiency.py 2017 ${syst_var}

  python calculate_btag_efficiency.py 2018 3 ${syst_var}
  python calculate_btag_efficiency.py 2018 4 ${syst_var}
  python calculate_btag_efficiency.py 2018 5 ${syst_var}
  python calculate_btag_efficiency.py 2018 7 ${syst_var}
  python presel_btag_efficiency.py 2018 ${syst_var}

  python calculate_btag_efficiency.py 2017p8 3 ${syst_var}
  python calculate_btag_efficiency.py 2017p8 4 ${syst_var}
  python calculate_btag_efficiency.py 2017p8 5 ${syst_var}
  python calculate_btag_efficiency.py 2017p8 7 ${syst_var}
  python presel_btag_efficiency.py 2017p8 ${syst_var}
done

echo "variant,ft,efft,frt" > efficiencies/all_effs.csv
cat efficiencies/effs_* >> efficiencies/all_effs.csv
rm efficiencies/effs_*
