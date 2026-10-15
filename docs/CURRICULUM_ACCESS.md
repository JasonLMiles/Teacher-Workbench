# Use your curriculum with Teacher Workbench

Start with:

> Use tw-curriculum-search. My curriculum is at [link, folder, repository, platform, or uploaded ebook]. Use [course/unit/edition] as the reference for [lesson, assessment, differentiation or substitute plan]. Guide me through any needed sign-in.

If you have not supplied a source, the skill asks where to look. It uses an existing connection where sufficient; otherwise it helps you find a supported provider integration or use an authorized browser route. Complete any login or school verification in the host's secure flow. You do not need to send passwords or verification codes in chat.

| Curriculum location | What the skill does | What the host needs |
| --- | --- | --- |
| Repository or district curriculum library | Searches and follows folders/files; records edition and revision where available. | A provider reader, authorized browser or supplied local files. |
| Assessment system or LMS | Opens authorized teacher reference resources and previews without starting tests or assigning work. | A supported connected provider tool or authorized browser plus your permitted account. |
| Website or publisher portal | Searches content and follows course/unit/lesson navigation and document viewers. | Public retrieval tools; interactive/private pages require browser capability and any necessary account access. |
| Ebook/PDF/EPUB | Reads relevant sections, contents and pages; preserves reliable page/chapter locators. | Uploaded readable files or an authorized online reader with supported file/browser tools. |
| Google Drive | Finds the supplied folder/shared drive, follows results and opens source documents. | A sufficient authorized Drive connection or a permitted browser route. |
| SharePoint/OneDrive | Resolves the site/library/drive/folder, searches and opens actual documents. | A sufficient authorized Microsoft connection or a permitted browser route. |

The result is a compact reference pack with actual content findings, source links, edition, unit/lesson/page, access date and gaps. Lesson, assessment, cross-curricular, differentiation, language-support and substitute skills reuse it. Restricted links are marked “requires your account.” Uploaded files receive file/section citations when no stable online link exists. Source content, independently verified California standards, research evidence and proposed adaptations remain distinguishable.

The skill defaults to relevant reads. It does not change grades, launch assessments, assign work, alter permissions or redistribute a licensed curriculum. It respects the teacher's AI preference. You may choose public references or original resources instead of providing a private curriculum.

## Portability and connection requirements
Teacher Workbench 1.2.0 is a skills-only plugin. It includes navigation instructions and reference templates, not a bundled browser, Drive/Microsoft connector, publisher account or hosted MCP service. Available integrations and account permissions depend on the destination host and school policy. Each user connects their own authorized account. The skill discovers real capabilities and clearly identifies an unsupported operation; it cannot create access by prompting alone. If a source cannot be opened, it can work with a permitted upload/export or clearly labeled alternative.

This follows [OpenAI's separation of skills and tool/authentication capabilities](https://developers.openai.com/plugins/concepts/skills). Plugin layout follows [the official packaging guide](https://developers.openai.com/plugins/build/plugins). For provider navigation details and checked primary links, see the [provider playbooks](../skills/tw-curriculum-search/references/provider-playbooks.md).

## Verification scope
The release includes fresh behavior checks for source intake, actual local curriculum retrieval and EPUB chapter/section retrieval. These checked edition selection, usable citations and ignoring an embedded instruction that conflicts with the teacher's task. Live school/publisher sign-in, Google Drive/SharePoint accounts and interactive website navigation have not been tested with your accounts. Validate those paths in your destination host before depending on them for classroom work; use the [review cases](REVIEW_TEST_CASES.md).

## Uploaded planning documents and resource production
Use `tw-curriculum-document-intake` after access/read to reconcile scope-and-sequence, curriculum and lesson documents with your conversation. Uploads can be used without a login. For consistent lesson/substitute plans, teaching aids, scaffolding, reflection/tracking, PBIS and Google Sheets/Canva production, see [teaching workflows](TEACHING_WORKFLOWS.md).
