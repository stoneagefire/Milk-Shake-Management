import json
import os
from os import system

dict1_in = {}
dict1_in1 = {}
item_list = []
order_detail = []
qty_track = []
final_order_list = []
summary_view = []


def create_item_menu():

    with open('items.json') as f:
        data = json.load(f)

    for i in data['items']:
        item_list.append([i['id'], i['name'], i['type'], i['price'], 0])
        qty_track.append([i['id'], i['available_quantity']])
    
    for i in range(len(qty_track)):
        if qty_track[i] == 0:
            item_list.remove(qty_track[i])


def create_order():
    create_item_menu()
    while(True):

        # Base item selection

        print("--------------------------------")
        print("\tBase Items")
        print("--------------------------------")
        menu_item_ct = 0
        for i in item_list:
            if i[2] == 'base':
                menu_item_ct += 1
                print("{0}. {1}".format(menu_item_ct, i[1]))
        print("--------------------------------")
        base_item_choice = int(input("Enter choice number : "))

        if base_item_choice > 3:
            print("Invalid choice number")
        else:
            if base_item_choice == 1:
                item_list[0][4] += 1
                qty_track[0][1] -= 1
                order_detail.append(item_list[0][:4])
                print(item_list[0][1], "selected")

            elif base_item_choice == 2:
                item_list[1][4] += 1
                qty_track[1][1] -= 1
                order_detail.append(item_list[1][:4])
                print(item_list[1][1], "selected")

            elif base_item_choice == 3:
                item_list[2][4] += 1
                qty_track[2][1] -= 1
                order_detail.append(item_list[2][:4])
                print(item_list[2][1], "selected")

            else:
                print("Invalid base item choice")

        print("--------------------------------")
        print("\tAddOn Items")
        print("--------------------------------")
        menu_item_ct = 0
        for i in item_list:
            if i[2] == 'addon':
                menu_item_ct += 1
                print("{0}. {1}".format(menu_item_ct, i[1]))
        print("--------------------------------")

        addon_item = int(
            input("No. of addon items you want to put\n(maximum 3 addons) : "))
        count1 = 0

        while count1 < addon_item:
            print("--------------------------------")
            print("\tAddOn Items")
            print("--------------------------------")
            menu_item_ct = 0
            for i in item_list:
                if i[2] == 'addon':
                    menu_item_ct += 1
                    print("{0}. {1}".format(menu_item_ct, i[1]))
            print("5. Done")
            print("--------------------------------")
            addon_item_choice = int(input("Enter choice number : "))

            if addon_item_choice == 0:
                break

            elif addon_item_choice == 1:
                item_list[3][4] += 1
                qty_track[3][1] -= 1
                order_detail.append(item_list[3][:4])
                print(item_list[3][1], "selected")
                count1 += 1

            elif addon_item_choice == 2:
                item_list[4][4] += 1
                qty_track[4][1] -= 1
                order_detail.append(item_list[4][:4])
                print(item_list[4][1], "selected")
                count1 += 1

            elif addon_item_choice == 3:
                item_list[5][4] += 1
                qty_track[5][1] -= 1
                order_detail.append(item_list[5][:4])
                print(item_list[5][1], "selected")
                count1 += 1

            elif addon_item_choice == 4:
                item_list[6][4] += 1
                qty_track[6][1] -= 1
                order_detail.append(item_list[6][:4])
                print(item_list[6][1], "selected")
                count1 += 1

            elif addon_item_choice == 5:
                break

            else:
                print("Invalid item choice..")
        break

    payment_sum = 0
    print("------------------------------------------------------")
    print("\tItem\t\t|  Qty  |   Price")
    print("------------------------------------------------------")
    for i in item_list:
        if i[4] == 0:
            continue
        else:
            if len(i[1]) > 14:
                print(i[1], "\t|", i[4], '\t|', (i[3]*i[4]))
            else:
                print(i[1], "\t\t|", i[4], '\t|', (i[3]*i[4]))
            payment_sum += i[3]*i[4]

    print("------------------------------------------------------")
    print("Total :", payment_sum)
    print("\n 1. Confirm\n 2. Cancel")
    order_count = 0

    while True:
        order_confirmed = int(input("Enter choice : "))
        if order_confirmed == 1:
            temp_list = []
            for i in item_list:
                if i[4] == 0:
                    continue
                else:
                    temp_list.append(i)
            final_order_list.append([temp_list, payment_sum])
            system('cls')
            print("Order placed")
            order_count += 1
            break

        elif order_confirmed == 2:
            print("Order cancelled")
            order_detail.clear()
            break

        else:
            print("Invalid choice")
            continue


def order_string():
    create_order()
    with open("orders.json", "r") as f:
        order = json.load(f)

    index = len(order['orders'])

    index2 = 0
    for i in final_order_list:
        for j in range(len(i)-1):
            str2 = str(index)
            dict1_in1['order '+str2] = []
            for k in range(len(i[j])):
                str1 = str(index2+1)
                dict1_in['item '+str1] = {}
                dict1_in['item '+str1] = {
                    'id': i[j][k][0],
                    'name': i[j][k][1],
                    'type': i[j][k][2],
                    'price': i[j][k][3],
                    'quantity': i[j][k][4]
                }
                # index += 1
                index2 += 1
            dict1_in1['order '+str2].append(dict1_in)
            dict1_in1['order '+str2].append({'total': final_order_list[len(
                final_order_list)-1][len(final_order_list[len(final_order_list)-1])-1]})
            index2 += 1

        order['orders'].append(dict1_in1)

    with open('orders.json', 'w') as f:
        json.dump(order, f, indent=4)


def stock_info():
    stock_dict = []

    with open('orders.json') as f:
        orders = json.load(f)

    with open('sam.json') as f:
        stock = json.load(f)

    index = len(orders['orders'])
    new_index = 0

    for i in orders['orders']:
        for j in range(len(i)):
            next_index = len(i['order '+str(new_index)][0])
            for k in i['order '+str(new_index)][0]:
                for l in i['order '+str(new_index)][0][k]:
                    if l == 'name':
                        stock_dict.append([
                            i['order '+str(new_index)][0][k][l],
                            i['order '+str(new_index)][0][k]['price'],
                            i['order '+str(new_index)][0][k]['quantity']
                        ])
            next_index -= 1
            new_index += 1

    item_1 = 0
    item_2 = 0
    item_3 = 0
    item_4 = 0
    item_5 = 0
    item_6 = 0
    item_7 = 0
    itemQty = []

    for i in stock_dict:
        if i[0] == 'Chocolate Milk':
            item_1 += i[2]
        elif i[0] == 'Kesar Milk':
            item_2 += i[2]
        elif i[0] == 'Faluda Milk':
            item_3 += i[2]
        elif i[0] == 'Icecream Scoop':
            item_4 += i[2]
        elif i[0] == 'Rose Petals':
            item_5 += i[2]
        elif i[0] == 'Chocolate chips':
            item_6 += i[2]
        elif i[0] == 'Faluda Milk':
            item_7 += i[2]

    itemQty.append([item_1, item_2, item_3, item_4, item_5, item_6, item_7])

    print(itemQty)

    index = 0
    for i in stock['items']:
        i['available_quantity'] -= itemQty[0][index]
        index += 1

    index = 0
    for i in stock['items']:
        if itemQty[0][index] == 0:
            index += 1
            continue
        else:
            amt = itemQty[0][index] * i['price']
            summary_view.append(
                [i['name'], itemQty[0][index], i['available_quantity'], amt])
            index += 1

    with open('stock.json', 'w') as f:
        json.dump(stock, f, indent=4)

    return summary_view


def view_summary():
    stock_dict = []
    summary_view = []
    with open('orders.json') as f:
        orders = json.load(f)

    with open('items.json') as f:
        stock = json.load(f)

    if len(orders) == 0:
        print("Zero orders found")
    else:
        index = len(orders['orders'])
        new_index = 0

        for i in orders['orders']:
            for j in range(len(i)):
                next_index = len(i['order '+str(new_index)][0])
                for k in i['order '+str(new_index)][0]:
                    for l in i['order '+str(new_index)][0][k]:
                        if l == 'name':
                            stock_dict.append([
                                i['order '+str(new_index)][0][k][l],
                                i['order '+str(new_index)][0][k]['price'],
                                i['order '+str(new_index)][0][k]['quantity']
                            ])
                next_index -= 1
                new_index += 1

        item_1 = 0
        item_2 = 0
        item_3 = 0
        item_4 = 0
        item_5 = 0
        item_6 = 0
        item_7 = 0
        itemQty = []

        for i in stock_dict:
            if i[0] == 'Chocolate Milk':
                item_1 += i[2]
            elif i[0] == 'Kesar Milk':
                item_2 += i[2]
            elif i[0] == 'Faluda Milk':
                item_3 += i[2]
            elif i[0] == 'Icecream Scoop':
                item_4 += i[2]
            elif i[0] == 'Rose Petals':
                item_5 += i[2]
            elif i[0] == 'Chocolate chips':
                item_6 += i[2]
            elif i[0] == 'Faluda Milk':
                item_7 += i[2]

        itemQty.append([item_1, item_2, item_3, item_4, item_5, item_6, item_7])

        index = 0
        for i in stock['items']:
            i['available_quantity'] -= itemQty[0][index]
            index += 1

        index = 0
        for i in stock['items']:
            if itemQty[0][index] == 0:
                index += 1
                continue
            else:
                amt = itemQty[0][index] * i['price']
                summary_view.append([i['name'], itemQty[0][index], i['available_quantity'], amt])
                index += 1

    total = 0
    print("\n------------------------------------------------------------")
    print("     Item   \t\t| Qty sold| Available Qty |  Sold Amount")
    print("------------------------------------------------------------")
    for i in summary_view:
        if len(i[0]) > 14:
            print(i[0], "\t|  ", i[1], "\t| ", i[2], "\t\t|", i[3])
        else:
            print(i[0], "\t\t|  ", i[1], "\t| ", i[2], "\t\t|", i[3])

        total += i[3]

    print("------------------------------------------------------------")
    print("Toal Revenue Generated :", total)


if __name__ == '__main__':

    while (True):
        print("\n------------------------------------------")
        print("\t  Milk Shake Maker")
        print("------------------------------------------")
        print(" 1. Create Order:")
        print(" 2. View Statistics")
        print(" 3. Exit")
        print("------------------------------------------")
        ch = int(input("\nEnter choice : "))

        if ch == 1:
            print("Create order section")
            order_string()
            # stock_info()

        elif ch == 2:
            view_summary()
            print("View Statistics section ")
        
        elif ch == 3:
            print("Thank you for visiting Milk shake shop")
            break

        else:
            print("Invalid choice...")
