using Microsoft.EntityFrameworkCore;
using TIA.Domain.Entities;
using TIA.Domain.Interfaces;
using TIA.Persistence.Context;

namespace TIA.Persistence.Repositories
{
    public class QuizRepository : BaseRepository<AppFile>, IQuizRepository
    {
        public QuizRepository(AppDbContext context) : base(context)
        { }

        public async Task<IEnumerable<Answear>> GetAnswersByQuestionIdAsync(Guid questionId, CancellationToken cancellationToken)
        {
            return await Context.Answears
                .Where(x => x.QuestionId == questionId)
                .ToListAsync();
        }

        public async Task<IEnumerable<Question>> GetQuestionsByQuizIdAsync(Guid fileId, CancellationToken cancellationToken)
        {
            return await Context.Questions.Where(x => x.FileId == fileId).ToListAsync();
        }
    }
}
