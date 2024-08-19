git filter-repo --commit-callback '
if commit.commit_id == b"282eb57f287f06a540156c0ef0d80c4e7c840fb9":
    commit.skip()'
