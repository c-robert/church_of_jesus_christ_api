[
  {
    unitNumber: int,
    orgUuids: [
      str
    ],
    weeks: [
      {
        week: str,
        visitors: {
          men: int,
          women: int,
          youngMen: int,
          youngWomen: int
        },
        attended: [
          str
        ],
        editable: bool
      }
    ],
    permissions: [
      str
    ]
  }
]