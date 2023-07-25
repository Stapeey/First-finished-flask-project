from website import create_app

app = create_app()

if __name__ == '__main__': 
    app.run(debug=True)

#potential errors:
#   when page is closed without logging out, you will still be logged in
#   time zones are not configured
#   special characters might break registration, database, login, notes
#   no password recovery
#   cant delete account