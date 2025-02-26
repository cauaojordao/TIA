using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IAnswear
    {
        Guid QuestionId { get; set; }
        Question Question { get; set; }
        string Text { get; set; }
        bool IsCorrect { get; set; }
    }
}
