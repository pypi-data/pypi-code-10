# -*- coding: utf-8 -*-

"""Utilities for getting/creating/listing files on a branch."""

from base64 import b64decode
from .internals import (blobs, commits, refs, trees)


def prepare(data):
    """Format blob data for output."""
    result = {}
    result["mode"] = data.get("mode")
    result["path"] = data.get("path")
    result["type"] = data.get("type")
    result["sha"] = data.get("sha")
    return result


def get_branch_sha(profile, name):
    """Get the SHA a branch's HEAD points to."""
    ref = "heads/" + name
    data = refs.get_ref(profile, ref)
    head = data.get("head")
    sha = head.get("sha")
    return sha


def get_commit_tree(profile, sha):
    """Get the SHA of a commit's tree."""
    data = commits.get_commit(profile, sha)
    tree = data.get("tree")
    sha = tree.get("sha")
    return sha


def get_files_in_tree(profile, sha):
    """Get the files (blobs) in a tree."""
    data = trees.get_tree(profile, sha)
    tree = data.get("tree")
    blobs = [x for x in tree if x.get("type") == "blob"]
    return blobs


def remove_file_from_tree(tree, file_path):
    """Remove a file from a tree."""
    match = None
    for item in tree:
        if item.get("path") == file_path:
            match = item
            break
    if match:
        tree.remove(match)
    return tree


def add_file_to_tree(tree, file_path, file_contents, is_executable=False):
    """Add a file to a tree."""
    record = {
        "path": file_path,
        "mode": "100755" if is_executable else "100644",
        "type": "blob",
        "content": file_contents,
        }
    tree.append(record)
    return tree


def get_files_in_branch(profile, branch_sha):
    """Get all files in a branch's tree."""
    tree_sha = get_commit_tree(profile, branch_sha)
    files = get_files_in_tree(profile, tree_sha)
    tree = [prepare(x) for x in files]
    return tree

def list_files(profile, branch):
    """List all files on a branch."""
    branch_sha = get_branch_sha(profile, branch)
    return get_files_in_branch(branch_sha)


def add_file(profile, branch, file_path, file_contents, is_executable=False, commit_message=None):
    """Add a file to a branch."""
    branch_sha = get_branch_sha(profile, branch)
    tree = get_files_in_branch(profile, branch_sha)
    new_tree = add_file_to_tree(tree, file_path, file_contents, is_executable)
    data = trees.create_tree(profile, new_tree)
    sha = data.get("sha")
    if not commit_message:
        commit_message = "Added " + file_path + "."
    parents = [branch_sha]
    commit_data = commits.create_commit(profile, commit_message, sha, parents)
    commit_sha = commit_data.get("sha")
    ref_data = refs.update_ref(profile, "heads/" + branch, commit_sha)
    return ref_data


def delete_file(profile, branch, file_path, commit_message=None):
    """Remove a file from a branch."""
    branch_sha = get_branch_sha(profile, branch)
    tree = get_files_in_branch(profile, branch_sha)
    new_tree = remove_file_from_tree(tree, file_path)
    data = trees.create_tree(profile, new_tree)
    sha = data.get("sha")
    if not commit_message:
        commit_message = "Deleted " + file_path + "."
    parents = [branch_sha]
    commit_data = commits.create_commit(profile, commit_message, sha, parents)
    commit_sha = commit_data.get("sha")
    ref_data = refs.update_ref(profile, "heads/" + branch, commit_sha)
    return ref_data


def get_file(profile, branch, file_path):
    """Get a file from a branch."""
    branch_sha = get_branch_sha(profile, branch)
    tree = get_files_in_branch(profile, branch_sha)
    match = None
    for item in tree:
        if item.get("path") == file_path:
            match = item
            break
    file_sha = match.get("sha")
    blob = blobs.get_blob(profile, file_sha)
    content = blob.get("content")
    decoded_content = b64decode(content)
    return decoded_content.decode("utf-8")
