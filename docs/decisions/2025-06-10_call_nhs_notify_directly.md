# Summary

We’ve decided to simplify the technical approach for the Bowel Cancer Screening System (BCSS) pre-invitation notifications by sending messages directly via NHS Notify, rather than routing them through the Comms Manager platform.

## Rationale

-Simplifies the overall design - avoids the need to build integration points between BCSS and Comms Manager
-Reduces the scope of work - fewer moving parts means less time spent on implementation and testing
-Minimises risk - removes a potential point of failure in the notification chain
-Faster delivery - avoids unnecessary dependencies, enabling quicker progress

## Outcome

The change allows us to deliver value sooner, with a clearer and more manageable implementation path. This decision is specific to the BCSS pre-invitations workflow and does not affect how Comms Manager can be used in other screening programmes, nor does it prevent changing BCSS to use Comms Manager at a later date if this is deemed useful.

## Potential Concerns

*Q: Does this represent a waste of effort?*
*A:* Not in engineering terms, no. Documentation and understanding needs to be updated, but in terms of engineering effort, switching to a direct-to-Notify solution is minimal (and actually saves effort in establishing communication between AWS and Azure)

*Q: What's the impact on reporting?*
*A:* For BCSS in the immediate term there should be no impact on reporting - because BCSS's Oracle database still records the changes in status, it will still be possible to understand how many people were sent app messages and read them, versus how many people were sent app messages and didn't. As that's the only thing happening in the Pre-Invitations piece of work, we don't see that there'd be any impact on reporting here. Basically, any reporting that could have been done on the Pre-Invitations piece of work by Comms Manager should also be able to be inferred from the data held in BCSS.

*Q: If BCSS wants to use Comms Manager in future, can they?*
*A:* Absolutely - nothing here is a introducing a dead-end at all, but given the overall direction of delivering value tactically ahead of producing re-usable components, this is in our opinion the correct choice for right now.