# REVIEW.md — what reviewers (human or AI) must check

**What failure looks like in this repo: "it smears, or it lies."** A fact that is unsourced, unlabelled, over-collected (private life), or framed as wrongdoing without evidence and a right of reply.

Check, in this order, citing file:line as evidence:

1. **Labels and sources:** does every new fact have a label? Does every fact that is not Unknown or Withheld (POPIA) have a dated source URL? Are Unknown and Withheld (POPIA) fields explicit nulls, with no public URL on a withheld fact?
2. **Public role only:** no ID numbers, home addresses, personal phones or emails, private family, or health information. Official office contacts only.
3. **Right of reply:** every adverse item has a `right_of_reply` object, a draft on disk, and legal status fields. Pending shows "Right of reply: pending" and a blank reply field. The bot must not have sent anything.
4. **Neutrality:** no opinion adjectives; claims are attributed; institutional findings stay on the council unless a source names the person.
5. **Provenance:** raw downloads have sha256 and a manifest entry. Roster rows cite a gazette page.
6. **Counts:** Joburg roster still reconciles to 270 / 135 / 135 unless a later official correction is sourced.
7. **Security:** no secrets, no new wild access, new packages verified.
8. **Tests:** a regression test for every rule or bug fixed. Pytest uses synthetic fixtures; do not add live-network tests.

Rules:

- Cap nits at 3.
- Skip gitignored raw PDFs.
- Start the summary with a count of findings, and say plainly when there is nothing to fix.
- Tag findings Important / Nit / Pre-existing.
- A review of a named head is a plain PASS or it is not a PASS. `PASS_WITH_CONCERNS` does not count.
