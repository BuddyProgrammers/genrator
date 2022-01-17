import requests
ip = '172.105.41.126:8000'


def add_user(first_name: str, last_name: str, passw: str, phone_no: int):
    pload = {
        "user_id": "",
        "first_name": first_name,
        "last_name": last_name,
        "phone_no": phone_no,
        "encrypted_password": passw
    }
    r = requests.post(f'http://{ip}/t_teacher', json=pload, headers={
                      "accept": "application/json", "Content-Type": "application/json"})
    print(r.json())


def check(teacher_id: int, entered_passw: str = ""):
    pload = {
        "teacher_id": teacher_id,
        "entered_passw": entered_passw,
    }
    r = requests.get(f'http://{ip}/check_passwt?teacherid={pload["teacher_id"]}&entered_passw={pload["entered_passw"]}', headers={
                     "accept": "application/json", "Content-Type": "application/json"})
    print(r.json())
    return r.json()


def genotp(phone_no: int):
    pload = {
        "phone_no": phone_no
    }
    r = requests.get(f'http://{ip}/get_otp?phone_no={pload["phone_no"]}', headers={
                     "accept": "application/json", "Content-Type": "application/json"})

    return r.json()
# add_user(
#             first_name= "gopal",
#             last_name= "Tapori" ,
#             passw="1234",
#             phone_no= 1234567890 ,
#             location = "1.2345,12.123"
#             )
