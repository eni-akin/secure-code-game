#include "code.h"
#include <assert.h>
#include <limits.h>

int main(void) {
    int user = create_user_account(false, "student");
    assert(user == 0);
    assert(!update_setting(user, "-7", "1"));
    assert(!update_setting(user, "10", "1"));
    assert(!update_setting(user, "", "1"));
    assert(!update_setting(user, "0", ""));
    assert(!update_setting(user, "99999999999999999999999999", "1"));
    assert(!update_setting(user, "0", "99999999999999999999999999"));
    assert(!update_setting(99, "0", "1"));
    assert(!is_admin(99));
    assert(username(99) == NULL);
    assert(!update_setting(user, NULL, "1"));
    assert(create_user_account(false, NULL) == INVALID_USER_ID);
    assert(update_setting(user, "9", "10"));
    assert(!is_admin(user));
    for (int i = 1; i < MAX_USERS; ++i)
        assert(create_user_account(false, "student") == i);
    assert(create_user_account(false, "overflow") == INVALID_USER_ID);
    for (int i = 0; i < MAX_USERS; ++i) free(accounts[i]);
    puts("PASS: Level 2 bounds, numeric parsing, account capacity, and privilege checks");
}
