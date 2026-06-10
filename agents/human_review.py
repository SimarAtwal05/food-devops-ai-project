def human_review(state):

    print("\n")
    print("=" * 60)
    print("PROPOSED FIX")
    print("=" * 60)

    print(state["patch"])

    answer = input(
        "\nApprove Fix? (yes/no): "
    )

    return {
        "approved":
        answer.lower() == "yes"
    }