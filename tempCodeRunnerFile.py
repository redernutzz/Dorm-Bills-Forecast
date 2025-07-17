    global num_months
        if num_months > 0 and len(electricity) > 0:
            row_index = len(electricity) - 1

            try:
                # Destroy the month label in the same row
                month_label = scrollable_frame.grid_slaves(row=num_months, column=0)[0]
                month_label.destroy()

                # Destroy and remove other widgets
                electricity[row_index].destroy()
                water[row_index].destroy()
                groceries[row_index].destroy()

                # Remove from lists
                electricity.pop(row_index)
                water.pop(row_index)
                groceries.pop(row_index)

                # Decrement num_months
                num_months -= 1

                # Reposition remaining widgets if any exist
                for i in range(row_index):
                    # Reposition month labels
                    month_labels = scrollable_frame.grid_slaves(column=0)
                    if i < len(month_labels):
                        month_labels[len(month_labels)-1-i].grid(row=i+1, column=0, padx=10, pady=10, sticky="w")
                    
                    # Reposition other entries
                    electricity[i].grid(row=i+1, column=1, padx=10, pady=10, sticky="w")
                    water[i].grid(row=i+1, column=2, padx=30, pady=10, sticky="w")
                    groceries[i].grid(row=i+1, column=3, padx=30, pady=10, sticky="w")

                # Update scroll region
                scrollable_frame.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
            
            except IndexError:
                print("No more months to delete")
            except Exception as e:
                print(f"Error deleting month: {e}")
        else:
            print("No months to delete")