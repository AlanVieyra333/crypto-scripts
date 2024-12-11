#!python3
# Proceso para analizar el total de las facturas recibidas durante el mes.

import sys
import os
import os.path
from optparse import OptionParser
from xml.dom import minidom
import glob
import pandas as pd

def main(argv):
 
    usage = "%prog [opciones] <path_metadata_file>"
    parser = OptionParser(usage=usage, add_help_option=False)
    parser.add_option("-h", "--help", action="help",
        help=u"Muestra este mensaje de ayuda y termina")
    parser.add_option("-t", "--type", default="I",
        action="store", type="string", dest="VOUCHER_TYPE",
        help=u"Especifica el tipo de comprobante que se analizara: I, E, N o X [default: %default]")
    (options, args) = parser.parse_args()
 
    if len(args) == 0:
        parser.error("Se tiene que indicar el nombre del archivo de metadatos")
    else:
        pathMetadata = args[0]
 
    if not os.path.isfile(pathMetadata):
        print("El archivo " + pathMetadata + " no existe, vuelve a intentarlo!")
        sys.exit(1)
 
    df = pd.read_csv(pathMetadata, delimiter='~', engine='python', encoding='utf-8', on_bad_lines='warn')
    df = df[df["FechaCancelacion"].isnull()]
    df = df[["Uuid", "RfcEmisor", "Monto", "EfectoComprobante", "NombreEmisor"]]
    if options.VOUCHER_TYPE != 'X': # N - Nomina, E - Egreso, I - Ingreso
        df = df[df['EfectoComprobante'] == options.VOUCHER_TYPE]
        
    montoTotal = df['Monto'].sum()
    print(df.sort_values(by=['Monto']).to_string())
    print("\nMonto total: " + str(montoTotal))

 
if __name__ == "__main__":
  main(sys.argv[1:])
