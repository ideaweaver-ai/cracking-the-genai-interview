from collections import defaultdict
from typing import List


class Solution:
    # Time: O(A*log(A)), A = sum(ai) - ai = accounts[i]
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:

        def find(i):
            parent.setdefault(i, i)
            rank.setdefault(i, 0)

            if parent[i] != i:
                parent[i] = find(parent[i])

            return parent[i]

        def union(x, y):
            # Defualt parent and rank set in find
            xset = find(x)
            yset = find(y)

            if xset != yset:
                if rank[xset] > rank[yset]:
                    parent[yset] = xset
                elif rank[yset] > rank[xset]:
                    parent[xset] = yset
                else:
                    parent[yset] = xset
                    rank[xset] += 1

        parent = {}
        rank = {}

        email_name_map = {}

        # we want to perform union on emails, as connected emails mean the same person
        # # same name may not mean the same person
        # we want a mapping of email to name to create the result
        for account in accounts:
            name = account[0]
            emails = account[1:]

            for email in emails:
                email_name_map[email] = name
                union(email, emails[0])

        # once we have the parents lets connect all nodes belonging to same connected component
        # lets connect all emails belonging to same person
        connected_emails = defaultdict(list)
        for email in parent:
            connected_emails[find(email)].append(email)

        # Output formatting
        merged_accounts = []
        for main_email, all_emails in connected_emails.items():
            account = []
            account.append(email_name_map[main_email])
            # since emails need to be sorted
            all_emails = sorted(all_emails)
            for email in all_emails:
                account.append(email)
            merged_accounts.append(account)

        return merged_accounts


if __name__ == '__main__':
    accounts = [["John", "johnsmith@mail.com", "john00@mail.com"], ["John", "johnnybravo@mail.com"],
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["Mary", "mary@mail.com"]]

    output = [["John", 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'],  ["John", "johnnybravo@mail.com"], ["Mary", "mary@mail.com"]]

    sol = Solution()
    assert sol.accountsMerge(accounts) == output, "Incorrect o/p"