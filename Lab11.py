import matplotlib.pyplot as plt
import os

def load_assignments(file_path):
    assignments = []
    with open("data/assignments.txt", "r") as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            assignment_id = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments.append({"name": name, "id": assignment_id, "points": points})
    return assignments

def load_students(file_path):
    students = []
    with open("data/students.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            student_id = int(line[:3])
            name = line[3:].strip()
            students.append({"id": student_id, "name": name})
    return students

def load_submissions(folder_path):
    submissions_data = []
    for file_name in os.listdir("data/submissions"):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    student_code, assignment_code, score_percentage = line.strip().split("|")
                    submissions_data.append({
                        "student_id": int(student_code),
                        "assignment_id": int(assignment_code),
                        "percentage": float(score_percentage)
                    })
    return submissions_data


def get_student_grade(student_name, students, submissions, assignments):
    student = next((s for s in students if s["name"] == student_name), None)
    if not student:
        print("Student not found")
        return

    total_points = 0
    earned_points = 0
    for submission in submissions:
        if submission["student_id"] == student["id"]:
            assignment = next((a for a in assignments if a["id"] == submission["assignment_id"]), None)
            if assignment:
                total_points += assignment["points"]
                earned_points += (submission["percentage"] / 100) * assignment["points"]

    grade = round((earned_points / total_points) * 100)
    print(f"{grade}%")

def get_assignment_statistics(assignment_name, assignments, submissions):
    assignment = next((a for a in assignments if a["name"] == assignment_name), None)
    if not assignment:
        print("Assignment not found")
        return

    scores = [
        submission["percentage"]
        for submission in submissions
        if submission["assignment_id"] == assignment["id"]
    ]
    if scores:
        print(f"Min: {min(scores):.0f}%")
        print(f"Avg: {int(sum(scores) / len(scores))}%")
        print(f"Max: {max(scores):.0f}%")

def plot_assignment_histogram(assignment_name, assignments, submissions):
    assignment = next((a for a in assignments if a["name"] == assignment_name), None)
    if not assignment:
        print("Assignment not found")
        return

    scores = [
        submission["percentage"]
        for submission in submissions
        if submission["assignment_id"] == assignment["id"]
    ]
    if scores:
        plt.hist(scores, bins=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100], edgecolor='black')
        plt.title(f"Histogram for {assignment_name}")
        plt.xlabel("Score Ranges (%)")
        plt.ylabel("Frequency")
        plt.show()

def main():
    assignments_data = load_assignments("data/assignments.txt")
    students_data = load_students("data/students.txt")
    submissions_data = load_submissions("data/submissions")

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ").strip()

    if choice == "1":
        student_name = input("What is the student's name: ").strip()
        get_student_grade(student_name, students_data, submissions_data, assignments_data)
    elif choice == "2":
        assignment_name = input("What is the assignment name: ").strip()
        get_assignment_statistics(assignment_name, assignments_data, submissions_data)
    elif choice == "3":
        assignment_name = input("What is the assignment name: ").strip()
        plot_assignment_histogram(assignment_name, assignments_data, submissions_data)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
