# Password is qwerty, if new password is desired, run this code and follow the steps
# from crypt import crypt
# password = "" # Enter the password you want
# key = "" # Enter a 2 character key here
# print crypt(password, key)
# Step 1: Copy the output and paste that information in the password column
# Step 2: Copy the key and paste that information in the pass_key column

# Todo Section Test Data
INSERT INTO users (username, firstname, lastname, password, pass_key) VALUE ('dev', 'Developer', 'McDev', '00YfpO1MXDzqQ', '00');
INSERT INTO users (username, firstname, lastname, password, pass_key) VALUE ('test', 'Developer2', 'McDeveloper', '00YfpO1MXDzqQ', '00');

INSERT INTO priorities (severity, name, color) VALUE (1, 'Highest', 'FF0000');
INSERT INTO priorities (severity, name, color) VALUE (2, 'High', '996600');
INSERT INTO priorities (severity, name, color) VALUE (3, 'Normal', '55AA00');
INSERT INTO priorities (severity, name, color) VALUE (4, 'Low', '22CC00');
INSERT INTO priorities (severity, name, color) VALUE (5, 'Lowest', '00FF00');
INSERT INTO priorities (severity, name, color) VALUE (6, 'Soon', 'FFFFFF')

INSERT INTO categories (name, color) VALUE ('Test1', 'FF2222');
INSERT INTO categories (name, color) VALUE ('Test2', '009999');
INSERT INTO categories (name, color) VALUE ('Test3', '990099');
INSERT INTO categories (name, color) VALUE ('Test4', '6633FF');
INSERT INTO categories (name, color) VALUE ('Test5', 'FF6633');
INSERT INTO categories (name, color) VALUE ('Test6', '0000FF');

INSERT INTO tasks (task, user_id, created) VALUE ("One", 1, '2009-12-03 10:10:00');
INSERT INTO tasks (task, user_id, created) VALUE ("Two", 1, '2009-12-03 10:10:01');
INSERT INTO tasks (task, user_id, created) VALUE ("Three", 1, '2009-12-03 10:10:02');
INSERT INTO tasks (task, user_id, created) VALUE ("Four", 1, '2009-12-03 10:10:03');
INSERT INTO tasks (task, user_id, created) VALUE ("Five", 1, '2009-12-03 10:10:04');
INSERT INTO tasks (task, user_id, created) VALUE ("Six", 1, '2009-12-03 10:10:05');

INSERT INTO tasks (task, user_id, created) VALUE ("One", 2, '2009-12-03 10:10:00');
INSERT INTO tasks (task, user_id, created) VALUE ("Two", 2, '2009-12-03 10:10:01');
INSERT INTO tasks (task, user_id, created) VALUE ("Three", 2, '2009-12-03 10:10:02');
INSERT INTO tasks (task, user_id, created) VALUE ("Four", 2, '2009-12-03 10:10:03');
INSERT INTO tasks (task, user_id, created) VALUE ("Five", 2, '2009-12-03 10:10:04');
INSERT INTO tasks (task, user_id, created) VALUE ("Six", 2, '2009-12-03 10:10:05');

INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "One" LIMIT 1), (SELECT id FROM priorities WHERE severity = 1 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Two" LIMIT 1), (SELECT id FROM priorities WHERE severity = 2 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Three" LIMIT 1), (SELECT id FROM priorities WHERE severity = 3 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Four" LIMIT 1), (SELECT id FROM priorities WHERE severity = 4 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Five" LIMIT 1), (SELECT id FROM priorities WHERE severity = 5 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Six" LIMIT 1), (SELECT id FROM priorities WHERE severity = 6 LIMIT 1));

INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "One" LIMIT 1), (SELECT id FROM priorities WHERE severity = 1 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Two" LIMIT 1), (SELECT id FROM priorities WHERE severity = 2 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Three" LIMIT 1), (SELECT id FROM priorities WHERE severity = 3 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Four" LIMIT 1), (SELECT id FROM priorities WHERE severity = 4 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Five" LIMIT 1), (SELECT id FROM priorities WHERE severity = 5 LIMIT 1));
INSERT INTO task_to_priority_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Six" LIMIT 1), (SELECT id FROM priorities WHERE severity = 6 LIMIT 1));

INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "One" LIMIT 1), (SELECT id FROM categories WHERE name = "Test1" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Two" LIMIT 1), (SELECT id FROM categories WHERE name = "Test2" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Three" LIMIT 1), (SELECT id FROM categories WHERE name = "Test3" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Four" LIMIT 1), (SELECT id FROM categories WHERE name = "Test4" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Five" LIMIT 1), (SELECT id FROM categories WHERE name = "Test5" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 1 and task = "Six" LIMIT 1), (SELECT id FROM categories WHERE name = "Test6" LIMIT 1));

INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "One" LIMIT 1), (SELECT id FROM categories WHERE name = "Test1" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Two" LIMIT 1), (SELECT id FROM categories WHERE name = "Test2" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Three" LIMIT 1), (SELECT id FROM categories WHERE name = "Test3" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Four" LIMIT 1), (SELECT id FROM categories WHERE name = "Test4" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Five" LIMIT 1), (SELECT id FROM categories WHERE name = "Test5" LIMIT 1));
INSERT INTO task_to_category_xref (task_id, priority_id) VALUE ((SELECT id FROM tasks WHERE user_id = 2 and task = "Six" LIMIT 1), (SELECT id FROM categories WHERE name = "Test6" LIMIT 1));

# Question/Blog Section Test Data
INSERT INTO questions (created, question, user_id, public) VALUE ('2009-12-03 10:10:10', 'Something Public and viewed from User 1', 1, 1);
INSERT INTO questions (created, question, user_id, public) VALUE ('2009-12-03 10:10:10', 'Something Public and not viewed by User 2', 1, 1);
INSERT INTO questions (created, question, user_id, public) VALUE ('2009-12-03 10:10:10', 'Something Private for User 1 only', 1, 0);
INSERT INTO questions (created, question, user_id, public) VALUE ('2009-12-03 10:10:10', 'Something Public and viewed from User 2', 2, 1);
INSERT INTO questions (created, question, user_id, public) VALUE ('2009-12-03 10:10:10', 'Something Public and not viewed by User 1', 2, 1);
INSERT INTO questions (created, question, user_id, public) VALUE ('2009-12-03 10:10:10', 'Something Private for User 2 only', 2, 0);

# For testing Purposes I am going to use the same reponses, but in reality this should never happen in the system
INSERT INTO responses (created, response, user_id) VALUE ('2009-12-03 10:10:10', "Some random response by User 1", 1);
INSERT INTO responses (created, response, user_id) VALUE ('2009-12-03 10:10:10', "Some random response by User 2", 2);

INSERT INTO responses_to_question_xref (question_id, response_id) VALUE ((SELECT id FROM questions WHERE user_id = 1 AND public = 0LIMIT 1), (SELECT id FROM responses WHERE user_id = 1 LIMIT 1));
INSERT INTO responses_to_question_xref (question_id, response_id) VALUE ((SELECT id FROM questions WHERE user_id = 1 AND question = 'Something Public and viewed from User 1'LIMIT 1), (SELECT id FROM responses WHERE user_id = 1 AND response = "Some random response by User 1" LIMIT 1));
INSERT INTO responses_to_question_xref (question_id, response_id) VALUE ((SELECT id FROM questions WHERE user_id = 1 AND question = 'Something Public and not viewed by User 2' LIMIT 1), (SELECT id FROM responses WHERE user_id = 1 AND response = "Some random response by User 1" LIMIT 1));
INSERT INTO responses_to_question_xref (question_id, response_id) VALUE ((SELECT id FROM questions WHERE user_id = 2 AND public = 0LIMIT 1), (SELECT id FROM responses WHERE user_id = 1 LIMIT 1));
INSERT INTO responses_to_question_xref (question_id, response_id) VALUE ((SELECT id FROM questions WHERE user_id = 2 AND question = 'Something Public and viewed from User 2'LIMIT 1), (SELECT id FROM responses WHERE user_id = 2 AND response = "Some random response by User 2" LIMIT 1));
INSERT INTO responses_to_question_xref (question_id, response_id) VALUE ((SELECT id FROM questions WHERE user_id = 2 AND question = 'Something Public and not viewed by User 1' LIMIT 1), (SELECT id FROM responses WHERE user_id = 2 AND response = "Some random response by User 2" LIMIT 1));

INSERT INTO user_views_of_question_xref (question_id, user_id, last_viewed) VALUE ((SELECT id FROM questions WHERE user_id = 1 and public = 1 and question = 'Something Public and viewed from User 1' LIMIT 1), 2, '2009-12-03 10:10:11');
INSERT INTO user_views_of_question_xref (question_id, user_id, last_viewed) VALUE ((SELECT id FROM questions WHERE user_id = 1 and public = 1 and question = 'Something Public and viewed from User 2' LIMIT 1), 1, '2009-12-03 10:10:11');

INSERT INTO comments (created, comment, user_id) VALUE ('2009-12-03 10:10:10', "Some random comment by User 1", 1);
INSERT INTO comments (created, comment, user_id) VALUE ('2009-12-03 10:10:10', "Some random comment by User 2", 2);

INSERT INTO comments_to_response_xref (comment_id, response_id) VALUE ((SELECT id FROM comments WHERE user_id = 1 LIMIT 1), (SELECT id FROM responses WHERE user_id = 1 LIMIT 1));
INSERT INTO comments_to_response_xref (comment_id, response_id) VALUE ((SELECT id FROM comments WHERE user_id = 2 LIMIT 1), (SELECT id FROM responses WHERE user_id = 2 LIMIT 1));

# Health Section Test Data
INSERT INTO units (unit, digest) VALUE ('Pounds', 'lbs');
INSERT INTO units (unit, digest) VALUE ('Kilograms', 'kgs');

INSERT INTO weights (weight, units, user_id, created) VALUE (190, (SELECT id FROM units WHERE unit = 'Pounds' LIMIT 1), 1, '2009-11-03 10:10:10');
INSERT INTO weights (weight, units, user_id, created) VALUE (200, (SELECT id FROM units WHERE unit = 'Pounds' LIMIT 1), 1, '2009-12-03 10:10:10');
INSERT INTO weights (weight, units, user_id, created) VALUE (180, (SELECT id FROM units WHERE unit = 'Pounds' LIMIT 1), 2, '2009-11-03 10:10:10');
INSERT INTO weights (weight, units, user_id, created) VALUE (200, (SELECT id FROM units WHERE unit = 'Pounds' LIMIT 1), 2, '2009-12-03 10:10:10');