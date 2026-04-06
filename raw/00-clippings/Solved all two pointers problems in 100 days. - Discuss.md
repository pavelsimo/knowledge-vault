---
title: "Solved all two pointers problems in 100 days. - Discuss"
source: "https://leetcode.com/discuss/post/1688903/solved-all-two-pointers-problems-in-100-z56cn/"
author:
published:
created: 2026-04-06
description: "Hello, I have been solving all two pointers tagged problems in last 3.5 months, and wanted to share my findings/classifications here. If you are preparing for"
tags:
  - "clippings"
---
Solved all two pointers problems in 100 days.

[Two Pointers](https://leetcode.com/discuss/topic/two-pointers/) [Career](https://leetcode.com/discuss/topic/career/)

Hello,  
I have been solving all two pointers tagged problems in last 3.5 months, and wanted to share my findings/classifications here. If you are preparing for technical interview, two pointers is one of the popular topics that you can't skip:).

There are around 140 problems today, but I only solved the public ones (117 problems).  
Majority of them is in easy or medium so, if you understand the basic ideas then it should be solvable without much hints and editorials.

I see 4 bigger categories and many sub categories in it, and marked the typical example problems with (\*).  
I would recommend you to start solving these example problems, and apply the knowledge to the other problems. I don't want to copy & paste my ugly codes here, you would easily find fantastic solutions from the problem discussion page.

  

| 1\. Running from both ends of an array |
| --- |
| The first type of problems are, having two pointers at left and right end of array, then moving them to the center while processing something with them. |
| ![[raw/00-clippings/images/bdc48f21ed66c89229d9fb6aca4d4760_MD5.jpg]] |

- 2 Sum problem  
	(\*) [https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)  
	[https://leetcode.com/problems/3sum/](https://leetcode.com/problems/3sum/)  
	[https://leetcode.com/problems/4sum/](https://leetcode.com/problems/4sum/)  
	[https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/](https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/)  
	[https://leetcode.com/problems/two-sum-iv-input-is-a-bst/](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/)  
	[https://leetcode.com/problems/sum-of-square-numbers/](https://leetcode.com/problems/sum-of-square-numbers/)  
	[https://leetcode.com/problems/boats-to-save-people/](https://leetcode.com/problems/boats-to-save-people/)  
	[https://leetcode.com/problems/minimize-maximum-pair-sum-in-array/](https://leetcode.com/problems/minimize-maximum-pair-sum-in-array/)  
	[https://leetcode.com/problems/3sum-with-multiplicity/](https://leetcode.com/problems/3sum-with-multiplicity/)
- Trapping Water  
	(\*) [https://leetcode.com/problems/trapping-rain-water/](https://leetcode.com/problems/trapping-rain-water/)  
	[https://leetcode.com/problems/container-with-most-water/](https://leetcode.com/problems/container-with-most-water/)
- Next Permutation  
	(\*) [https://leetcode.com/problems/next-permutation/](https://leetcode.com/problems/next-permutation/)  
	[https://leetcode.com/problems/next-greater-element-iii/](https://leetcode.com/problems/next-greater-element-iii/)  
	[https://leetcode.com/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/](https://leetcode.com/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/)
- Reversing / Swapping  
	[https://leetcode.com/problems/valid-palindrome/](https://leetcode.com/problems/valid-palindrome/)  
	(\*) [https://leetcode.com/problems/reverse-string/](https://leetcode.com/problems/reverse-string/)  
	[https://leetcode.com/problems/reverse-vowels-of-a-string/](https://leetcode.com/problems/reverse-vowels-of-a-string/)  
	[https://leetcode.com/problems/valid-palindrome-ii/](https://leetcode.com/problems/valid-palindrome-ii/)  
	[https://leetcode.com/problems/reverse-only-letters/](https://leetcode.com/problems/reverse-only-letters/)  
	[https://leetcode.com/problems/remove-element/](https://leetcode.com/problems/remove-element/)  
	[https://leetcode.com/problems/sort-colors/](https://leetcode.com/problems/sort-colors/)  
	[https://leetcode.com/problems/flipping-an-image/](https://leetcode.com/problems/flipping-an-image/)  
	[https://leetcode.com/problems/squares-of-a-sorted-array/](https://leetcode.com/problems/squares-of-a-sorted-array/)  
	[https://leetcode.com/problems/sort-array-by-parity/](https://leetcode.com/problems/sort-array-by-parity/)  
	[https://leetcode.com/problems/sort-array-by-parity-ii/](https://leetcode.com/problems/sort-array-by-parity-ii/)  
	[https://leetcode.com/problems/pancake-sorting/](https://leetcode.com/problems/pancake-sorting/)  
	[https://leetcode.com/problems/reverse-prefix-of-word/](https://leetcode.com/problems/reverse-prefix-of-word/)  
	[https://leetcode.com/problems/reverse-string-ii/](https://leetcode.com/problems/reverse-string-ii/)  
	[https://leetcode.com/problems/reverse-words-in-a-string/](https://leetcode.com/problems/reverse-words-in-a-string/)  
	[https://leetcode.com/problems/reverse-words-in-a-string-iii/](https://leetcode.com/problems/reverse-words-in-a-string-iii/)
- Others  
	[https://leetcode.com/problems/bag-of-tokens/](https://leetcode.com/problems/bag-of-tokens/)  
	[https://leetcode.com/problems/di-string-match/](https://leetcode.com/problems/di-string-match/)  
	[https://leetcode.com/problems/minimum-length-of-string-after-deleting-similar-ends/](https://leetcode.com/problems/minimum-length-of-string-after-deleting-similar-ends/)  
	[https://leetcode.com/problems/sentence-similarity-iii/](https://leetcode.com/problems/sentence-similarity-iii/)  
	[https://leetcode.com/problems/find-k-closest-elements/](https://leetcode.com/problems/find-k-closest-elements/)  
	[https://leetcode.com/problems/shortest-distance-to-a-character/](https://leetcode.com/problems/shortest-distance-to-a-character/)
  

| 2.Slow & Fast Pointers |
| --- |
| Next type is using two pointers with different speed of movement. Typically they starts from the left end, then the first pointer advances fast and give some feedback to the slow pointer and do some calculation. |
| ![[raw/00-clippings/images/c64516269bdf98f4fd00322b3d31d526_MD5.jpg]] |

- Linked List Operations  
	(\*) [https://leetcode.com/problems/linked-list-cycle/](https://leetcode.com/problems/linked-list-cycle/)  
	[https://leetcode.com/problems/linked-list-cycle-ii/](https://leetcode.com/problems/linked-list-cycle-ii/)  
	[https://leetcode.com/problems/remove-nth-node-from-end-of-list/](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)  
	[https://leetcode.com/problems/rotate-list/](https://leetcode.com/problems/rotate-list/)  
	[https://leetcode.com/problems/reorder-list/](https://leetcode.com/problems/reorder-list/)  
	[https://leetcode.com/problems/palindrome-linked-list/](https://leetcode.com/problems/palindrome-linked-list/)
- Cyclic Detection  
	(\*) [https://leetcode.com/problems/find-the-duplicate-number/](https://leetcode.com/problems/find-the-duplicate-number/)  
	[https://leetcode.com/problems/circular-array-loop/](https://leetcode.com/problems/circular-array-loop/)
- Sliding Window/Caterpillar Method  
	![[raw/00-clippings/images/55651f4f134df003aec73d8f17e679f8_MD5.jpg]]  
	(\*) [https://leetcode.com/problems/number-of-subarrays-with-bounded-maximum/](https://leetcode.com/problems/number-of-subarrays-with-bounded-maximum/)  
	[https://leetcode.com/problems/find-k-th-smallest-pair-distance/](https://leetcode.com/problems/find-k-th-smallest-pair-distance/)  
	[https://leetcode.com/problems/moving-stones-until-consecutive-ii/](https://leetcode.com/problems/moving-stones-until-consecutive-ii/)  
	[https://leetcode.com/problems/count-pairs-of-nodes/](https://leetcode.com/problems/count-pairs-of-nodes/)  
	[https://leetcode.com/problems/count-binary-substrings/](https://leetcode.com/problems/count-binary-substrings/)  
	[https://leetcode.com/problems/k-diff-pairs-in-an-array/](https://leetcode.com/problems/k-diff-pairs-in-an-array/)
- Rotation  
	(\*) [https://leetcode.com/problems/rotating-the-box/](https://leetcode.com/problems/rotating-the-box/)  
	[https://leetcode.com/problems/rotate-array/](https://leetcode.com/problems/rotate-array/)
- String  
	(\*) [https://leetcode.com/problems/string-compression/](https://leetcode.com/problems/string-compression/)  
	[https://leetcode.com/problems/last-substring-in-lexicographical-order/](https://leetcode.com/problems/last-substring-in-lexicographical-order/)
- Remove Duplicate  
	(\*) [https://leetcode.com/problems/remove-duplicates-from-sorted-array/](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)  
	[https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/](https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/)  
	[https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/)  
	[https://leetcode.com/problems/duplicate-zeros/](https://leetcode.com/problems/duplicate-zeros/)
- Others  
	[https://leetcode.com/problems/statistics-from-a-large-sample/](https://leetcode.com/problems/statistics-from-a-large-sample/)  
	[https://leetcode.com/problems/partition-labels/](https://leetcode.com/problems/partition-labels/)  
	[https://leetcode.com/problems/magical-string/](https://leetcode.com/problems/magical-string/)  
	[https://leetcode.com/problems/friends-of-appropriate-ages/](https://leetcode.com/problems/friends-of-appropriate-ages/)  
	[https://leetcode.com/problems/longest-mountain-in-array/](https://leetcode.com/problems/longest-mountain-in-array/)  
	[https://leetcode.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted/](https://leetcode.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted/)
  

| 3.Running from beginning of 2 arrays / Merging 2 arrays |
| --- |
| In this category, you will be given 2 arrays or lists, then have to process them with individual pointers. |
| ![[raw/00-clippings/images/089618889f220be63e75aea935a14c9a_MD5.jpg]] |

- Sorted arrays  
	(\*) [https://leetcode.com/problems/merge-sorted-array/](https://leetcode.com/problems/merge-sorted-array/)  
	[https://leetcode.com/problems/heaters/](https://leetcode.com/problems/heaters/)  
	[https://leetcode.com/problems/find-the-distance-value-between-two-arrays/](https://leetcode.com/problems/find-the-distance-value-between-two-arrays/)
- Intersections/LCA like  
	(\*) [https://leetcode.com/problems/intersection-of-two-linked-lists/](https://leetcode.com/problems/intersection-of-two-linked-lists/)  
	[https://leetcode.com/problems/intersection-of-two-arrays/](https://leetcode.com/problems/intersection-of-two-arrays/)  
	[https://leetcode.com/problems/intersection-of-two-arrays-ii/](https://leetcode.com/problems/intersection-of-two-arrays-ii/)
- SubString  
	(\*) [https://leetcode.com/problems/implement-strstr/](https://leetcode.com/problems/implement-strstr/)  
	[https://leetcode.com/problems/longest-word-in-dictionary-through-deleting/](https://leetcode.com/problems/longest-word-in-dictionary-through-deleting/)  
	[https://leetcode.com/problems/long-pressed-name/](https://leetcode.com/problems/long-pressed-name/)  
	[https://leetcode.com/problems/longest-uncommon-subsequence-ii/](https://leetcode.com/problems/longest-uncommon-subsequence-ii/)  
	[https://leetcode.com/problems/compare-version-numbers/](https://leetcode.com/problems/compare-version-numbers/)  
	[https://leetcode.com/problems/camelcase-matching/](https://leetcode.com/problems/camelcase-matching/)  
	[https://leetcode.com/problems/expressive-words/](https://leetcode.com/problems/expressive-words/)
- Median Finder  
	(\*) [https://leetcode.com/problems/find-median-from-data-stream/](https://leetcode.com/problems/find-median-from-data-stream/)
- Meet-in-the-middle / Binary Search  
	(\*) [https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/)  
	[https://leetcode.com/problems/closest-subsequence-sum/](https://leetcode.com/problems/closest-subsequence-sum/)  
	[https://leetcode.com/problems/ways-to-split-array-into-three-subarrays/](https://leetcode.com/problems/ways-to-split-array-into-three-subarrays/)  
	[https://leetcode.com/problems/3sum-closest/](https://leetcode.com/problems/3sum-closest/)  
	[https://leetcode.com/problems/valid-triangle-number/](https://leetcode.com/problems/valid-triangle-number/)
- Others  
	[https://leetcode.com/problems/shortest-unsorted-continuous-subarray/](https://leetcode.com/problems/shortest-unsorted-continuous-subarray/)  
	[https://leetcode.com/problems/most-profit-assigning-work/](https://leetcode.com/problems/most-profit-assigning-work/)  
	[https://leetcode.com/problems/largest-merge-of-two-strings/](https://leetcode.com/problems/largest-merge-of-two-strings/)  
	[https://leetcode.com/problems/swap-adjacent-in-lr-string/](https://leetcode.com/problems/swap-adjacent-in-lr-string/)
  

| 4.Split & Merge of an array / Divide & Conquer |
| --- |
| The last one is similiar to previous category but there is one thing is added. First, you need to split the given list into 2 separate lists and then do two pointers approach to merge or unify them. There aren't many tasks here. |
| ![[raw/00-clippings/images/fd0e17ec0787b31191914cb8cd00c638_MD5.jpg]] |

- Partition  
	(\*) [https://leetcode.com/problems/partition-list/](https://leetcode.com/problems/partition-list/)
- Sorting  
	(\*) [https://leetcode.com/problems/sort-list/](https://leetcode.com/problems/sort-list/)

Comments (111)

Thank you. I am going to bookmark this, just like all the other top posts and never read again.

791

Show 9 Replies

Reply

[Abdul Malik](https://leetcode.com/u/buildwithmalik/)

Jan 15, 2022

Someone please give this guy an award.

194

Show 1 Replies

Reply

[Aakash Raj](https://leetcode.com/u/aakashraj/)

Jan 15, 2022

Thanks for sharing in proper way. Giving 3.5 month on a topic and after that sharing your hard work with others is really appreciated.

144

Show 1 Replies

Reply

[Abdul Malik](https://leetcode.com/u/buildwithmalik/)

Jan 17, 2022

Can someone make a leetcode list of these problems please?

42

Show 2 Replies

Reply

[Ajay Rao](https://leetcode.com/u/ajayraorao05/)

Jan 20, 2022

Thanks for segregating problems. A big upvote. Did you do the same for other topics as well?

28

Reply

Thanks. This is great. I find it very helpful to focus on a single technique and zero in on it for awhile. Posts like this are really helpful.

17

Reply

[Shefali Prajapati](https://leetcode.com/u/PrajapatiShefali/)

Feb 26, 2022

A need of such lists on graphs and trees please!!!!!! Thanks in advance

14

Show 4 Replies

Reply

Thanks for sharing. Appreciate your time in compiling this list.

9

Reply

Thanks OP. How much time did you spent per problem.

8

Show 1 Replies

Reply

This post is gold! Thank you so much brother!

7

Reply