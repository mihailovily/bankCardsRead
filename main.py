readed_info = open("card_data.txt", "r").read()
second_stripe = readed_info.split(';')[-1]
second_stripe = second_stripe.split("=")
pan = second_stripe[0]
other_data = second_stripe[1]
valid_until = other_data[2:4]+".20"+other_data[0:2]
service_code = other_data[4:7]
pvki = other_data[7]
pvv = other_data[8:12]
cvv1 = other_data[12:15]
print(f"\nPAN: {pan}\nValid until: {valid_until}\nService code: {service_code}\nPVKI: {pvki}\nPVV: {pvv}\nCVV1: {cvv1}\n")
if service_code == "201":
    print("International Chip card\nNormal authorization processing\nNo terminal restrictions\n")