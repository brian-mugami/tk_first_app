from tkinter import *
import psycopg2 as pg
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title("Address Check")
root.geometry("400x400")

con = pg.connect(database="attendance", user="postgres", password="mugami", host="localhost", port="5432")
cur = con.cursor()

# create a db
"""
print("Creating")
cur.execute(
    "CREATE TABLE IF NOT EXISTS addresses(id SERIAL , first_name TEXT, last_name TEXT, address TEXT, city TEXT, state TEXT, zip_code INTEGER)")
print("Done")

con.commit()
cur.close()
con.close()
"""

f_name = Entry(root, width=30)
f_name_label = Label(root, text="First Name").grid(row=0, column=0)
f_name.grid(row=0, column=1, padx=20)

l_name = Entry(root, width=30)
l_name_label = Label(root, text="Last Name").grid(row=1, column=0)
l_name.grid(row=1, column=1, padx=20)

address = Entry(root, width=30)
address_label = Label(root, text="Address").grid(row=2, column=0)
address.grid(row=2, column=1, padx=20)

city = Entry(root, width=30)
city_label = Label(root, text="City").grid(row=3, column=0)
city.grid(row=3, column=1, padx=20)

state = Entry(root, width=30)
state_label = Label(root, text="State").grid(row=4, column=0)
state.grid(row=4, column=1, padx=20)

zip_code = Entry(root, width=30)
zip_label = Label(root, text="Zip Code").grid(row=5, column=0)
zip_code.grid(row=5, column=1, padx=20)


def submit_record():
    con = pg.connect(database="attendance", user="postgres", password="mugami", host="localhost", port="5432")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO addresses(first_name, last_name, city, address, state, zip_code) VALUES( %s, %s, %s, %s, %s, %s)",
        (f_name.get(), l_name.get(), city.get(), address.get(), state.get(), zip_code.get()))
    con.commit()
    con.close()

    f_name.delete(0, END)
    l_name.delete(0, END)
    city.delete(0, END)
    address.delete(0, END)
    zip_code.delete(0, END)
    state.delete(0, END)


def query_records():
    results = Toplevel()
    results.title("Record")
    cur.execute("SELECT * FROM addresses")
    all_records = cur.fetchall()
    Label(results, text="First Name").grid(row=0, column=0, padx=20, pady=10)
    Label(results, text="Last Name").grid(row=0, column=1, padx=20, pady=10)
    Label(results, text="Address").grid(row=0, column=2, padx=20, pady=10)
    Label(results, text="City").grid(row=0, column=3, padx=20, pady=10)
    Label(results, text="Country").grid(row=0, column=4, padx=20, pady=10)
    Label(results, text="Zip Code").grid(row=0, column=5, padx=20, pady=10)
    Label(results, text="Delete").grid(row=0, column=6, padx=20, pady=10)
    Label(results, text="Update").grid(row=0, column=7, padx=20, pady=10)

    def update_record(_id):
        cur.execute("SELECT * FROM addresses WHERE id = %s", (_id,))
        record_to_update = cur.fetchone()

        update = Toplevel()
        update.title("update record")

        f_name = Entry(update, width=30)
        Label(update, text="First Name").grid(row=0, column=0)
        f_name.insert(0, record_to_update[1])
        f_name.grid(row=0, column=1, padx=20)

        l_name = Entry(update, width=30)
        Label(update, text="Last Name").grid(row=1, column=0)
        l_name.insert(0, record_to_update[2])
        l_name.grid(row=1, column=1, padx=20)

        address = Entry(update, width=30)
        Label(update, text="Address").grid(row=2, column=0)
        address.insert(0, record_to_update[3])
        address.grid(row=2, column=1, padx=20)

        city = Entry(update, width=30)
        Label(update, text="City").grid(row=3, column=0)
        city.insert(0, record_to_update[4])
        city.grid(row=3, column=1, padx=20)

        state = Entry(update, width=30)
        Label(update, text="State").grid(row=4, column=0)
        state.insert(0, record_to_update[5])
        state.grid(row=4, column=1, padx=20)

        zip_code = Entry(update, width=30)
        Label(update, text="Zip Code").grid(row=5, column=0)
        zip_code.insert(0, record_to_update[6])
        zip_code.grid(row=5, column=1, padx=20)

        def update_row():
            cur.execute(
                "UPDATE addresses SET first_name = %s, last_name = %s, address = %s, city = %s, state = %s, zip_code = %s WHERE id = %s",
                (f_name.get(), l_name.get(), address.get(), city.get(), state.get(), zip_code.get(), _id))
            con.commit()
            messagebox.showinfo("Updated", "This record has been updated successfully!!")
            update.destroy()
            results.destroy()

        Button(update, text="Update", command=update_row, border=10).grid(row=6, column=0, ipadx=100,
                                                                          columnspan=2, pady=10, padx=10)

    def delete_record(_id):
        response = messagebox.askyesno("Are you sure",
                                       message="You are about to delete this record do you wish to proceed")
        if response == 1:
            cur.execute("DELETE FROM addresses WHERE id = %s", (_id,))

            con.commit()
            results.destroy()
        else:
            print("aborted")

    i = len(all_records)
    for record in all_records:
        Label(results, text=record[1]).grid(row=i, column=0)
        Label(results, text=record[2]).grid(row=i, column=1)
        Label(results, text=record[3]).grid(row=i, column=2)
        Label(results, text=record[4]).grid(row=i, column=3)
        Label(results, text=record[5]).grid(row=i, column=4)
        Label(results, text=record[6]).grid(row=i, column=5)
        Button(results, text="Delete", command=lambda: delete_record(record[0]), fg="red", background="grey").grid(
            row=i, column=6)
        Button(results, text="Update", command=lambda: update_record(record[0])).grid(row=i, column=7)
        i += 1


query_btn = Button(root, text="Show records", command=query_records)
query_btn.grid(row=7, column=1, columnspan=2, pady=20, padx=20, ipadx=100)

submit_button = Button(root, text="Add record", command=submit_record, background="grey", fg="white")
submit_button.grid(row=6, column=1, columnspan=2, pady=20, padx=20, ipadx=100)

delete_button = Button()
root.mainloop()
