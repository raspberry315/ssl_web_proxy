# --------------------------------------------------------
# rm_folder
# --------------------------------------------------------
rm_folder() {
	find -name "$1" -exec rm -rf {} \; | true
}

# --------------------------------------------------------
# delete site files
# --------------------------------------------------------
rm -f *.pem
rm -f *.csr
rm -f *.key
rm -f *.crt
rm -f *.pfx
rm -f .rnd

# --------------------------------------------------------
# remove rm_folder folder
# --------------------------------------------------------
rm_folder demoCA
