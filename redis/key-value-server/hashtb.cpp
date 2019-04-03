#include "hashtb.h"
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;


vector<string> split_str(const string& src, const string& delim) {
    vector<string> dst;
    string str = src;
    str += delim[0]; // 扩展字符串，方便分割最后一节
    string ::size_type start = 0, index;
    index = str.find_first_of(delim, start); //在str中查找(起始：start) delim的任意字符的第一次出现的位置
    while (index != string::npos) {
        dst.push_back(str.substr(start, index-start)); //substr(start, len)
        start = str.find_first_not_of(delim, index);
        if (start == string::npos)
            return dst;
        index = str.find_first_of(delim, start);
    }
    return dst;
}


/*
 * 存在的问题：不能正确的赋值；key只能是整形；初始化没做好；不能扩容缩容
 * */


template<class KeyType, class ValueType>
class HashTable {
private:
    struct Node {
        KeyType key;
        ValueType value;
        Node* next;
        Node(KeyType k, ValueType v,Node* n = NULL) : key(k), value(v),next(n) {};
        Node():next(NULL) {};
    };
    const int TABLE_SIZE;
    Node** table;
    int Hash(KeyType key) {
        // 限制了key只能是整形
        return key % TABLE_SIZE;
    };
public:
    HashTable(int size = 23):TABLE_SIZE(size) {
        table = new Node *[TABLE_SIZE];
        for (int i = 0; i < TABLE_SIZE; i++) {
            table[i] = new Node();              // 虽是KeyType类型，new Node(-1, -1, NULL);也能正常运行
            cout << table[i]->key << endl;
        }
    };
    ~HashTable() {
        for (int i = 0; i < TABLE_SIZE; i++) {
            Node* head = table[i];
            while (head != NULL) {
                Node* next = head->next;
                delete head;
                head = next;
            }
        }
        delete []table;
    };
    void push(KeyType key, ValueType value) {
        int index = Hash(key);
        Node* head = table[index];
        if(head->next==NULL)
        {
            cout << "init" << endl;
            head->key = key;
            head->value = value;
        }else
        {
            cout << "second" << endl;
            Node* newItem = new Node(key, value, NULL);
            head->next = newItem;
        }

    };
    void erase(KeyType key) {
        int index = Hash(key);
        Node* head = table[index];
        while (head->next != NULL) {
            if (head->next->key == key) {
                Node* tmp = head->next;
                head->next = head->next->next;
                delete tmp;
                break;
            }
            head = head->next;
        }
    };
    ValueType get(KeyType key) {
        int index = Hash(key);
        Node* head = table[index];
        while (head) {
            if (head->key == key) {
                return head->value;
            }
            head = head->next;
        }

        return ValueType();
    };

};

//
//int main()
//{
//    HashTable<int, char> map;
//    cout << map.get(50) << endl;
//    for (int i = 0; i < 50; i++) {
//        map.push(i, i * 10);
//    }
//    cout << "total is 100" << endl;
//    cout << map.get(5) << endl;
//    cout << map.get(6) << endl;
//    map.erase(60);
//    cout << map.get(6) << endl;
//}
