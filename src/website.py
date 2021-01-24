import os

def activate_website(key, address):
    print("\n")
    print(">>>>>>>>>>>>>>>>>>>>>>>> Activating website... <<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print("  => Adding SECRET_KEY back to settings.py...")
    with open('website/website/settings.py', 'r') as f:
        last_line = f.readlines()[-1]
        
    print("  => Starting the Django development server...")
    with open('src/website.sh', 'w') as rsh:
        rsh.write('''cd website/website \n''')
        if last_line[:10] != 'SECRET_KEY':
            rsh.write('''echo "''')
            rsh.write(key)
            rsh.write('''" >> settings.py \n''')
        rsh.write('''cd .. \n''')
        rsh.write('''python manage.py runserver \n''')
    os.system('bash src/website.sh')
    return
