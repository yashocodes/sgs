from fpdf import FPDF, XPos, YPos

# Function to calculate GPA and performance statistics
def calculate_gpa_and_statistics(subjects, grades, credits):
    total_points = 0
    total_credits = 0
    grade_points = {'O': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'Fail': 0}
    passed = 0
    failed = 0
    highest = 'Fail'
    lowest = 'O'
    highest_subject = ''
    lowest_subject = ''

    for i, (grade, credit) in enumerate(zip(grades, credits)):
        total_points += grade_points[grade] * credit
        total_credits += credit
        
        if grade != 'Fail':
            passed += 1
            if highest == 'Fail' or grade_points[grade] > grade_points[highest]:
                highest = grade
                highest_subject = subjects[i]
            if lowest == 'O' or grade_points[grade] < grade_points[lowest]:
                lowest = grade
                lowest_subject = subjects[i]
        else:
            failed += 1

    gpa = total_points / total_credits if total_credits > 0 else 0
    return gpa, passed, failed, highest, lowest, highest_subject, lowest_subject

# Function to generate a PDF report
def generate_pdf(name, reg_no, semester, gpa, passed, failed, highest, lowest, highest_subject, lowest_subject, subjects, grades, credits):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)

    # Institution Heading
    pdf.set_font("Helvetica", style='B', size=14)  # Set to bold
    pdf.cell(0, 10, "SRM INSTITUTE OF SCIENCE AND TECHNOLOGY", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 10, "B.Tech DEGREE EXAMINATION", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.cell(0, 10, "REPORT CARD", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    pdf.set_font("Helvetica", size=12)  # Set back to regular font
    pdf.ln(10)  # Line break

    # Student Details
    pdf.cell(0, 10, f"Name: {name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Register No: {reg_no}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Semester: {semester}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)  # Line break

    # Adding table header
    pdf.set_font("Helvetica", style='B', size=12)  # Set table header to bold
    pdf.cell(20, 10, 'S.No', border=1, align='C')
    pdf.cell(60, 10, 'Subject', border=1, align='C')
    pdf.cell(40, 10, 'Credits', border=1, align='C')
    pdf.cell(40, 10, 'Grade', border=1, align='C')
    pdf.cell(40, 10, 'Result', border=1, align='C')
    pdf.ln()  # Line break

    # Reset to regular font for table rows
    pdf.set_font("Helvetica", size=12)

    # Adding table rows
    for i in range(len(subjects)):
        result = 'Pass' if grades[i] != 'Fail' else 'Fail'
        pdf.cell(20, 10, str(i + 1), border=1, align='C')  # Serial number
        pdf.cell(60, 10, subjects[i], border=1, align='C')
        pdf.cell(40, 10, str(credits[i]), border=1, align='C')
        pdf.cell(40, 10, grades[i], border=1, align='C')
        pdf.cell(40, 10, result, border=1, align='C')
        pdf.ln()  # Line break for the next row

    # Summary Section
    pdf.cell(0, 10, "", new_x=XPos.LMARGIN, new_y=YPos.NEXT)  # Empty line
    pdf.cell(0, 10, f"GPA: {gpa:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Passed Subjects: {passed}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Failed Subjects: {failed}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Highest Grade: {highest} in {highest_subject}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Lowest Grade: {lowest} in {lowest_subject}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Save the PDF
    pdf.output("Student_Grading_Report.pdf")
    print("PDF generated successfully: 'Student_Grading_Report.pdf'")

# Function to validate inputs
def validate_input(prompt, expected_type=str, condition=lambda x: True):
    while True:
        user_input = input(prompt)
        try:
            value = expected_type(user_input)
            if condition(value):
                return value
            else:
                print("Input does not meet the required condition. Please try again.")
        except ValueError:
            print(f"Invalid input. Please enter a valid {expected_type.__name__}.")

# Main program execution
def main():
    # Collect student information with validation
    name = validate_input("Enter your name: ")
    reg_no = validate_input("Enter your register number: ")
    semester = validate_input("Enter your semester: ")

    subjects = []
    grades = []
    credits = []

    # Ask for number of subjects with validation
    num_subjects = validate_input("Enter the number of subjects: ", expected_type=int, condition=lambda x: x > 0)

    # Collect subject details with validation
    for _ in range(num_subjects):
        subject = validate_input("Enter subject name: ")
        grade = validate_input("Enter grade (O, A, B, C, D, E, Fail): ", condition=lambda x: x in ['O', 'A', 'B', 'C', 'D', 'E', 'Fail'])
        credit = validate_input("Enter credits for this subject: ", expected_type=int, condition=lambda x: x > 0)
        subjects.append(subject)
        grades.append(grade)
        credits.append(credit)

    # Calculate GPA and performance statistics
    gpa, passed, failed, highest, lowest, highest_subject, lowest_subject = calculate_gpa_and_statistics(subjects, grades, credits)

    # Generate PDF report
    generate_pdf(name, reg_no, semester, gpa, passed, failed, highest, lowest, highest_subject, lowest_subject, subjects, grades, credits)

    # After generating the report, allow options to modify inputs
    while True:
        print("\nOptions:")
        print("1. Add more subjects")
        print("2. Remove a subject")
        print("3. Exit")
        choice = validate_input("Choose an option (1/2/3): ", expected_type=int, condition=lambda x: x in [1, 2, 3])

        if choice == 1:
            new_subject = validate_input("Enter subject name: ")
            new_grade = validate_input("Enter grade (O, A, B, C, D, E, Fail): ", condition=lambda x: x in ['O', 'A', 'B', 'C', 'D', 'E', 'Fail'])
            new_credit = validate_input("Enter credits for this subject: ", expected_type=int, condition=lambda x: x > 0)
            subjects.append(new_subject)
            grades.append(new_grade)
            credits.append(new_credit)

            # Recalculate GPA and performance statistics
            gpa, passed, failed, highest, lowest, highest_subject, lowest_subject = calculate_gpa_and_statistics(subjects, grades, credits)
            generate_pdf(name, reg_no, semester, gpa, passed, failed, highest, lowest, highest_subject, lowest_subject, subjects, grades, credits)
        
        elif choice == 2:
            subject_to_remove = validate_input("Enter the name of the subject to remove: ")
            if subject_to_remove in subjects:
                index = subjects.index(subject_to_remove)
                subjects.pop(index)
                grades.pop(index)
                credits.pop(index)

                # Recalculate GPA and performance statistics
                gpa, passed, failed, highest, lowest, highest_subject, lowest_subject = calculate_gpa_and_statistics(subjects, grades, credits)
                generate_pdf(name, reg_no, semester, gpa, passed, failed, highest, lowest, highest_subject, lowest_subject, subjects, grades, credits)
            else:
                print("Subject not found.")

        elif choice == 3:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()
