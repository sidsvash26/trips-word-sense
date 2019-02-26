IMS_VERSION=0.9.2.1
mkdir ims
wget -qO- www.comp.nus.edu.sg/~nlp/sw/IMS_v${IMS_VERSION}.tar.gz | tar xvz -
mv ims_$IMS_VERSION/testPlain.bash
chmod +x ims/testPlain.bash
wget -qO- www.comp.nus.edu.sg/~nlp/sw/lib.tar.gz | tar xvz - -C ims
wget -qO- sterling8.d2.comp.nus.edu.sg/sw/models-MUN-SC-wn30.tar.gz | tar xvz - -C ims
