#ifndef HASH_CACHE_H
#define HASH_CACHE_H
#include <vector>
#include <unordered_map>
#include <fstream>
#include <string>

#define FAILED -1
using namespace std;
std::vector<std::string> split_str(const std::string& src, const std::string& delim);

template<class KeyType, class ValueType>
class HashTable {
private:

    const int TABLE_SIZE;
    Node** table;
    int Hash(KeyType key) {
        // 限制了key只能是整形
        return key % TABLE_SIZE;
    };
public:
    HashTable(int size = 23):TABLE_SIZE(size);
    ~HashTable() ;
    void push(KeyType key, ValueType value) ;
    void erase(KeyType key);
    ValueType get(KeyType key);

};

#endif
